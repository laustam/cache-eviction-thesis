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

#endif // MYHELPERS_H
