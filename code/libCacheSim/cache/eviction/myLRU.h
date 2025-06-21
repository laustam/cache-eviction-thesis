#ifndef MYLRU_H
#define MYLRU_H

#include <assert.h>
#include "../../include/libCacheSim/cache.h"
#include "../../dataStructure/hashtable/hashtable.h"
#include "myHelpers.h"

typedef struct {
    cache_obj_t *head; // head of queue
    cache_obj_t *tail; // tail of queue
} myLRU_params_t;

/* initialize all the variables */
cache_t *myLRU_init(const common_cache_params_t ccache_params, const char *cache_specific_params);

/* find an object in the cache, return the cache object if found, NULL otherwise, update_cache means whether update the cache state, e.g., moving object to the head of the queue */
cache_obj_t *myLRU_find(cache_t *cache, const request_t *req, const bool update_cache);

/* insert an object to the cache, return the cache object, this assumes the object is not in the cache */
cache_obj_t *myLRU_insert(cache_t *cache, const request_t *req);

/* find the object to be evicted, return the cache object, not used very often */
cache_obj_t *myLRU_to_evict(cache_t *cache, const request_t *req);

/* evict an object from the cache, req should not be used */
void myLRU_evict(cache_t *cache, const request_t *req);

/* remove an object from the cache, return true if the object is found and removed, note that this is used for user-triggered remove, eviction should use evict */
bool myLRU_remove(cache_t *cache, const obj_id_t obj_id);

#endif // MYLRU_H
