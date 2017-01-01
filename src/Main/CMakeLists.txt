file( GLOB MAIN_SRC ./*.cpp ./*.c ./*.cxx )
add_executable( Main ${MAIN_SRC} )

target_link_libraries( Main
    calc
)
