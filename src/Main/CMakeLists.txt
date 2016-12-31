file( GLOB MAIN_SRC ./*.cpp ./*.c ./*.cxx )
add_executable( Main ${MAIN_SRC} )

target_link_libraries( Main
    calc
)

add_custom_command(TARGET Main POST_BUILD COMMAND AllTests)
