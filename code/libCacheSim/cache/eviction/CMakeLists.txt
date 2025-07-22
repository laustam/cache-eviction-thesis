set(sourceC
        mySieve.c
        myLRU.c
        myFIFO.c
        FIFO.c
        LRU.c
        Sieve.c
)

add_library (evictionC ${sourceC})
target_link_libraries(evictionC cachelib dataStructure utils)
