#include "mySIEVE.h"

/* initialize all the variables */
cache_t *mySIEVE_init(const common_cache_params_t ccache_params, const char *cache_specific_params) {
    // init specific params needed for sieve
    mySIEVE_params_t *params = calloc(1, sizeof(mySIEVE_params_t));
    params->hand = NULL;
    params->head = NULL;
    params->tail = NULL;

    cache_t *cache = cache_struct_init("mySIEVE", ccache_params, cache_specific_params);
    cache->cache_init = mySIEVE_init;
    cache->cache_free = myCache_free;
    cache->get = myCache_get;
    cache->find = mySIEVE_find;
    cache->insert = mySIEVE_insert;
    cache->evict = mySIEVE_evict;
    cache->remove = mySIEVE_remove;
    cache->to_evict = mySIEVE_to_evict;
    cache->eviction_params = params;
    cache->obj_md_size = ccache_params.consider_obj_metadata; // TODO: is this correct? shouldn't this be sizeof mySIEVE_params_t?

    return cache;
}

/* find an object in the cache, return the cache object if found, NULL otherwise, update_cache means whether update the
 * cache state, e.g., moving object to the head of the queue */
cache_obj_t *mySIEVE_find(cache_t *cache, const request_t *req, const bool update_cache) {
    cache_obj_t *cache_obj = cache_find_base(
        cache, req, update_cache); // look up a given object (returns pointer to the obj or NULL if not found)

    if (!cache_obj) {
        return NULL;
    }

    if (update_cache) {
        cache_obj->mySIEVE.visited = true; // indicates object was accessed again (it is popular)
    }

    return cache_obj;
}

/* insert an object to the cache, return the cache object, this assumes the object is not in the cache */
cache_obj_t *mySIEVE_insert(cache_t *cache, const request_t *req) {
    mySIEVE_params_t *params = cache->eviction_params;
    return myCache_insert_head(cache, req, &params->head, &params->tail);
}

/* find the object to be evicted, return the cache object, not used very often */
cache_obj_t *mySIEVE_to_evict(cache_t *cache, const request_t *req) {
    mySIEVE_params_t *params = cache->eviction_params;
    cache_obj_t *start_obj = !params->hand ? params->tail : params->head;

    // if item pointed to by hand is unvisited, it can be evicted
    if (!start_obj->mySIEVE.visited) {
        return start_obj;
    }

    // otherwise, check if there are other unvisited items in the queue
    cache_obj_t *curr_obj = !start_obj->queue.prev ? params->tail : start_obj->queue.prev;

    while (curr_obj != start_obj) {
        if (!curr_obj->mySIEVE.visited) {
            return curr_obj;
        }
        curr_obj = !curr_obj->queue.prev ? params->tail : curr_obj->queue.prev;
    }

    return NULL;
}

/* evict an object from the cache, req should not be used */
void mySIEVE_evict(cache_t *cache, const request_t *req) {
    mySIEVE_params_t *params = cache->eviction_params;
    cache_obj_t *curr_obj = !params->hand ? params->tail : params->hand;

    // find object in cache that is unvisited
    while (curr_obj->mySIEVE.visited) {
        curr_obj->mySIEVE.visited = false;
        curr_obj = !curr_obj->queue.prev ? params->tail : curr_obj->queue.prev;
    }

    // update hand + remove unvisited object from cache
    params->hand = curr_obj->queue.prev;
    remove_obj_from_list(&params->head, &params->tail, curr_obj);
    cache_evict_base(cache, curr_obj, true);
}

/* remove an object from the cache, return true if the object is found and removed, note that this is used for
 * user-triggered remove, eviction should use evict */
bool mySIEVE_remove(cache_t *cache, const obj_id_t obj_id) {
    cache_obj_t *cache_obj = hashtable_find_obj_id(cache->hashtable, obj_id);

    // cache obj not available
    if (!cache_obj) {
        return false;
    }

    mySIEVE_params_t *params = cache->eviction_params;

    // if we want to remove the item pointed to by the hand, move the hand first
    if (cache_obj == params->hand) {
        params->hand = cache_obj->queue.prev;
    }

    // remove cache obj
    remove_obj_from_list(&params->head, &params->tail, cache_obj);
    cache_remove_obj_base(cache, cache_obj, true);

    return true;
}
