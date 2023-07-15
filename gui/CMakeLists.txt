cmake_minimum_required(VERSION 3.15)

project(MSysMonitor LANGUAGES CXX)

set(CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/src/cmake)
include(qtprojectbuild)

project_version_patch_clean()

set(COMPANY "Radar-MMS")
set(COPYRIGHT "Copyright (c) 2023 ${COMPANY}. All rights reserved.")
set(IDENTIFIER "${PROJECT_NAME}")

add_project_meta(META_FILES)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(QT NAMES Qt5 REQUIRED COMPONENTS Core Quick)
find_package(Qt${QT_VERSION_MAJOR} REQUIRED COMPONENTS
  Core
  Quick
  Widgets
  Network
  QuickControls2
)

include_directories(src/c++ libs)

file(GLOB_RECURSE CPP_SOURCES
  #src/c++/*
)

set(PROJECT_SOURCES
  src/c++/main.c++
  src/c++/m_sys_monitor.h    src/c++/m_sys_monitor.c++

  #src/qml/qml.qrc
  #resources/resources.qrc
)

add_executable(${PROJECT_NAME}
  ${PROJECT_SOURCES}
  ${CPP_SOURCES}
  ${META_FILES}
)

#add_subdirectory here!

target_link_libraries(${PROJECT_NAME}
  PRIVATE Qt${QT_VERSION_MAJOR}::Core
  Qt${QT_VERSION_MAJOR}::Quick
  Qt${QT_VERSION_MAJOR}::Widgets
  Qt${QT_VERSION_MAJOR}::Network
  Qt${QT_VERSION_MAJOR}::QuickControls2
  )

install(TARGETS ${PROJECT_NAME}
  BUNDLE DESTINATION .
  LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
)

execute_process(COMMAND git remote update WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})
execute_process(COMMAND git describe --tags --abbrev=0 WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR} OUTPUT_VARIABLE GIT_VERSION OUTPUT_STRIP_TRAILING_WHITESPACE)

add_definitions(
  -DPROJECT_NAME="${PROJECT_NAME}"
  -DPROJECT_VERSION="${GIT_VERSION}"
  -DPROJECT_COMPANY="${COMPANY}"
)

message("${PROJECT_NAME} version ${PROJECT_VERSION} compiled successfully")

