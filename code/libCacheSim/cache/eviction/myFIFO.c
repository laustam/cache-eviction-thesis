#include "myFIFO.h"

/* initialize all the variables */
cache_t *myFIFO_init(const common_cache_params_t ccache_params, const char *cache_specific_params) {
    myFIFO_params_t *params = calloc(1, sizeof(myFIFO_params_t));
    params->head = NULL;
    params->tail = NULL;

    cache_t *cache = cache_struct_init("myFIFO", ccache_params, cache_specific_params);
    cache->cache_init = myFIFO_init;
    cache->cache_free = myCache_free;
    cache->get = myCache_get;
    cache->find = myFIFO_find;
    cache->insert = myFIFO_insert;
    cache->evict = myFIFO_evict;
    cache->remove = myFIFO_remove;
    cache->to_evict = myFIFO_to_evict;
    cache->eviction_params = params;

    return cache;
}

/* find an object in the cache, return the cache object if found, NULL otherwise, update_cache means whether update the cache state, e.g., moving object to the head of the queue */
cache_obj_t *myFIFO_find(cache_t *cache, const request_t *req, const bool update_cache) {
    // note: bool update_cache has no affect in FIFO (we never move items around)!
    return cache_find_base(cache, req, update_cache);
}

/* insert an object to the cache, return the cache object, this assumes the object is not in the cache */
cache_obj_t *myFIFO_insert(cache_t *cache, const request_t *req) {
    myFIFO_params_t *params = cache->eviction_params;
    return myCache_insert_head(cache, req, &params->head, &params->tail);
}

/* find the object to be evicted, return the cache object, not used very often */
cache_obj_t *myFIFO_to_evict(cache_t *cache, const request_t *req) {
    myFIFO_params_t *params = cache->eviction_params;
    return params->tail;
}

/* evict an object from the cache, req should not be used */
void myFIFO_evict(cache_t *cache, const request_t *req) {
    myFIFO_params_t *params = cache->eviction_params;
    myCache_evict_tail(cache, &params->head, &params->tail);
}

/* remove an object from the cache, return true if the object is found and removed, note that this is used for user-triggered remove, eviction should use evict */
bool myFIFO_remove(cache_t *cache, const obj_id_t obj_id) {
    myFIFO_params_t *params = cache->eviction_params;
    return myCache_remove_obj(cache, obj_id, &params->head, &params->tail);
}
