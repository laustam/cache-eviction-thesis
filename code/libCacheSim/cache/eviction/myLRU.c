#include "myLRU.h"

/* initialize all the variables */
cache_t *myLRU_init(const common_cache_params_t ccache_params, const char *cache_specific_params) {
    myLRU_params_t *params = calloc(1, sizeof(myLRU_params_t));
    params->head = NULL;
    params->tail = NULL;

    cache_t *cache = cache_struct_init("myLRU", ccache_params, cache_specific_params);
    cache->cache_init = myLRU_init;
    cache->cache_free = myCache_free;
    cache->get = myCache_get;
    cache->find = myLRU_find;
    cache->insert = myLRU_insert;
    cache->evict = myLRU_evict;
    cache->remove = myLRU_remove;
    cache->to_evict = myLRU_to_evict;
    cache->eviction_params = params;
    cache->obj_md_size = ccache_params.consider_obj_metadata ? 8 * 2 : 0; // TODO: is this correct? shouldn't this be sizeof myLRU_params_t?

    return cache;
}

/* find an object in the cache, return the cache object if found, NULL otherwise, update_cache means whether update the cache state, e.g., moving object to the head of the queue */
cache_obj_t *myLRU_find(cache_t *cache, const request_t *req, const bool update_cache) {
    cache_obj_t *cache_obj = cache_find_base(cache, req, update_cache);

    if (!cache_obj) {
        return NULL;
    }

    // if obj already exists in cache and the cache should be updated, move the obj to the head
    // the head contains newest items, the tail is where items are removed
    if (update_cache) {
        myLRU_params_t *params = cache->eviction_params;
        move_obj_to_head(&params->head, &params->tail, cache_obj);
    }

    return cache_obj;
}

/* insert an object to the cache, return the cache object, this assumes the object is not in the cache */
cache_obj_t *myLRU_insert(cache_t *cache, const request_t *req) {
    myLRU_params_t *params = cache->eviction_params;
    cache_obj_t *cache_obj = cache_insert_base(cache, req);       // insert obj (assuming it doesnt exist yet)
    prepend_obj_to_head(&params->head, &params->tail, cache_obj); // add the new obj to the head of the queue
    return cache_obj;
}

/* find the object to be evicted, return the cache object, not used very often */
cache_obj_t *myLRU_to_evict(cache_t *cache, const request_t *req) {
    // LRU always evict the oldest item (at the tail)
    myLRU_params_t *params = cache->eviction_params;
    return params->tail;
}

/* evict an object from the cache, req should not be used */
void myLRU_evict(cache_t *cache, const request_t *req) {
    myLRU_params_t *params = cache->eviction_params;
    assert(params->tail);

    cache_obj_t *evict_obj = params->tail; // evict oldest object at the tail
    params->tail = evict_obj->queue.prev;
    
    // edge case when queue is empty after removing single item in queue
    if (!params->tail) {
        params->head = NULL; // make sure head does not 
    }
    else {
        params->tail->queue.next = NULL;
    }

    // finally, evict base of cache (tail item)
    cache_evict_base(cache, evict_obj, true);
}

/* remove an object from the cache, return true if the object is found and removed, note that this is used for user-triggered remove, eviction should use evict */
bool myLRU_remove(cache_t *cache, const obj_id_t obj_id) {
    cache_obj_t *cache_obj = hashtable_find_obj_id(cache->hashtable, obj_id);

    if (!cache_obj) {
        return false;
    }

    myLRU_params_t *params = cache->eviction_params;

    remove_obj_from_list(&params->head, &params->tail, cache_obj);
    cache_remove_obj_base(cache, cache_obj, true);

    return true;
}
