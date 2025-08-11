#pragma once

#include "cache.h"

#ifdef __cplusplus
extern "C" {
#endif

/* used by LFU related */
typedef struct freq_node {
  int64_t freq;
  cache_obj_t *first_obj;
  cache_obj_t *last_obj;
  int32_t n_obj;
} freq_node_t;

typedef struct {
  cache_obj_t *q_head;
  cache_obj_t *q_tail;
  // clock uses one-bit counter
  int32_t n_bit_counter;
  // max_freq = 1 << (n_bit_counter - 1)
  int32_t max_freq;
  int32_t init_freq;

  int64_t n_obj_rewritten;
  int64_t n_byte_rewritten;
} Clock_params_t;

#ifdef __cplusplus
}
#endif
