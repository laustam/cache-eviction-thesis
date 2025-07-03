#ifndef MYHELPERS_H
#define MYHELPERS_H

#include "../../include/libCacheSim/cache.h"

/* free the resources used by the cache */
static inline void myCache_free(cache_t *cache) {
    if (cache->eviction_params) {
        free(cache->eviction_params);
    }
    cache_struct_free(cache);
}

/* get the object from the cache, it is find + on-demand insert/evict, return true if cache hit */
static inline bool myCache_get(cache_t *cache, const request_t *req) { 
    return cache_get_base(cache, req);
}

static inline cache_obj_t *myCache_insert_head(cache_t *cache, const request_t *req, cache_obj_t **head, cache_obj_t **tail) {
    cache_obj_t *cache_obj = cache_insert_base(cache, req);     // insert obj (assuming it doesnt exist yet)
    prepend_obj_to_head(head, tail, cache_obj);               // add the new obj to the head of the queue
    return cache_obj;
}

static inline void myCache_evict_tail(cache_t *cache, cache_obj_t **head, cache_obj_t **tail) {
    assert(*tail);

    cache_obj_t *evict_obj = *tail; // evict oldest object at the tail
    *tail = evict_obj->queue.prev;
    
    // edge case when queue is empty after removing single item in queue
    if (!*tail) {
        assert(cache->n_obj == 1);
        *head = NULL; // make sure head does not
    }
    else {
        assert(*tail);
        (*tail)->queue.next = NULL;
    }

    assert(*head || !*head);

    // finally, evict base of cache (tail item)
    cache_evict_base(cache, evict_obj, true);
}

static inline bool myCache_remove_obj(cache_t *cache, const obj_id_t obj_id, cache_obj_t **head, cache_obj_t **tail) {
    cache_obj_t *cache_obj = hashtable_find_obj_id(cache->hashtable, obj_id);

    if (!cache_obj) {
        return false;
    }

    remove_obj_from_list(head, tail, cache_obj);
    cache_remove_obj_base(cache, cache_obj, true);

    return true;
}

#endif // MYHELPERS_H
