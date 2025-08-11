set(sourceC
        mySIEVE.c
        myLRU.c
        myFIFO.c
)

add_library (evictionC ${sourceC})
target_link_libraries(evictionC cachelib dataStructure utils)
