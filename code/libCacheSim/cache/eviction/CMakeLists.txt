set(sourceC
        mySieve.c
        myLRU.c
        myFIFO.c
        FIFO.c
        LRU.c
        Sieve.c
)

set(sourceCPP
        cpp/LFU.cpp
        cpp/GDSF.cpp
        LHD/lhd.cpp
        LHD/LHD_Interface.cpp
        )

if (ENABLE_LRB)
    set (sourceCPP ${sourceCPP} 
        LRB/lrb.cpp
        LRB/LRB_Interface.cpp
        )
endif()

if (ENABLE_3L_CACHE)
    set (sourceCPP ${sourceCPP} 
        3LCache/ThreeLCache_Interface.cpp
        3LCache/ThreeLCache.cpp
        )
endif()

if (ENABLE_GLCACHE)
    set(sourceC 
        ${sourceC} 
        GLCache/bucket.c
        GLCache/dataPrep.c
        GLCache/eviction.c
        GLCache/GLCache.c
        GLCache/inference.c
        GLCache/init.c
        GLCache/segment.c
        GLCache/segSel.c
        GLCache/train.c
        )
endif()


add_library (evictionC ${sourceC})
target_link_libraries(evictionC cachelib dataStructure utils)
add_library (evictionCPP ${sourceCPP})
target_link_libraries(evictionCPP cachelib utils)
set_target_properties(evictionCPP
        PROPERTIES
        CXX_STANDARD 17
        CXX_STANDARD_REQUIRED YES
        CXX_EXTENSIONS NO
        )

# set (evictionLib
#         evictionC
#         evictionCPP
#         )


        
# add_library(eviction INTERFACE)
# target_link_libraries(eviction INTERFACE ${evictionLib})

