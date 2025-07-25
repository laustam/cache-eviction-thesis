
#include <strings.h>
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "../../include/libCacheSim/cache.h"
#include "../../include/libCacheSim/evictionAlgo.h"
#include "../../cache/eviction/mySIEVE.h"
#include "../../cache/eviction/myLRU.h"
#include "../../cache/eviction/myFIFO.h"

#ifdef __cplusplus
extern "C" {
#endif

static inline cache_t *create_cache(const char *trace_path, const char *eviction_algo, const uint64_t cache_size,
                                    const char *eviction_params, const bool consider_obj_metadata) {
  common_cache_params_t cc_params = {
    .cache_size = cache_size,
    .default_ttl = 86400 * 300,
    .hashpower = 24,
    .consider_obj_metadata = consider_obj_metadata,
};
  cache_t *cache;

  /* the trace provided is small */
  if (trace_path != NULL && strstr(trace_path, "data/trace.") != NULL) cc_params.hashpower -= 8;
  typedef struct {
    const char *name;
    cache_t *(*init_func)(common_cache_params_t, const char *);
  } eviction_algo_entry_t;

  static const eviction_algo_entry_t simple_algos[] = {
      {"my_sieve", mySIEVE_init},
      {"my_lru",  myLRU_init},
      {"my_fifo", myFIFO_init},
      {"lru", LRU_init},
      {"sieve", Sieve_init},
      {"fifo", FIFO_init}
  };

  cache_t *(*init_func)(common_cache_params_t, const char *) = NULL;
  for (size_t i = 0; i < sizeof(simple_algos) / sizeof(simple_algos[0]); ++i) {
    if (strcasecmp(eviction_algo, simple_algos[i].name) == 0) {
      init_func = simple_algos[i].init_func;
      break;
    }
  }

  if (init_func) {
    cache = init_func(cc_params, eviction_params);
  } else {
    ERROR("do not support algorithm %s\n", eviction_algo);
    abort();
  }

  return cache;
}

#ifdef __cplusplus
}
#endif
