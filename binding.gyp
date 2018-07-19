{
  "variables": {
    # may be redefined in command line on configuration stage
    # "BUILD_LIBRDKAFKA%": "<!(echo ${BUILD_LIBRDKAFKA:-1})"
    "BUILD_LIBRDKAFKA%": "<!(node ./util/get-env.js BUILD_LIBRDKAFKA 1)",
  },
  "targets": [
    {
      "target_name": "node-librdkafka",
      'sources': [
        'src/binding.cc',
        'src/callbacks.cc',
        'src/common.cc',
        'src/config.cc',
        'src/connection.cc',
        'src/errors.cc',
        'src/kafka-consumer.cc',
        'src/producer.cc',
        'src/topic.cc',
        'src/workers.cc'
      ],
      "include_dirs": [
        "<!(node -e \"require('nan')\")",
        "<(module_root_dir)/"
      ],
      'conditions': [
        [
          'OS=="win"',
          {
            'cflags_cc' : [
              '-std=c++11'
            ],
            'msvs_settings': {
              'VCLinkerTool': {
                'AdditionalDependencies': [
                  'librdkafka.lib',
                  'librdkafkacpp.lib'
                ],
                'AdditionalLibraryDirectories': [
                  'deps/librdkafka/win32/outdir/v120/x64/Release/'
                ]
              },
              'VCCLCompilerTool': {
                'AdditionalOptions': [
                  '/GR'
                ],
                'AdditionalUsingDirectories': [
                  'deps/librdkafka/win32/outdir/v120/x64/Release/'
                ],
                'AdditionalIncludeDirectories': [
                  'deps/librdkafka/src-cpp'
                ]
              }
            },
            'msvs_version': '2013',
            'msbuild_toolset': 'v120',
            "dependencies": [
              "deps/librdkafka.gyp:librdkafka"
            ],
            'include_dirs': [
              'deps/librdkafka/src-cpp'
            ]
          },
          {
            'conditions': [
              [ "<(BUILD_LIBRDKAFKA)==1",
                {
                  "dependencies": [
                    "deps/librdkafka.gyp:librdkafka"
                  ],
                  "include_dirs": [
                    "deps/librdkafka/src-cpp"
                  ],
                  'conditions': [
                    [
                      'OS=="linux"',
                      {
                        "libraries": [
                          "../build/deps/librdkafka.so",
                          "../build/deps/librdkafka++.so",
                          "-Wl,-rpath=build/deps",
                        ],
                      }
                    ],
                    [
                      'OS=="mac"',
                      {
                        "libraries": [
                          "../build/deps/librdkafka.dylib",
                          "../build/deps/librdkafka++.dylib",
                        ],
                      }
                    ]
                  ],
                },
                # Else link against globally installed rdkafka and use
                # globally installed headers.  On Debian, you should
                # install the librdkafka1, librdkafka++1, and librdkafka-dev
                # .deb packages.
                {
                  "libraries": ["-lrdkafka", "-lrdkafka++"],
                  "include_dirs": [
                    "/usr/include/librdkafka",
                    "/usr/local/include/librdkafka"
                  ],
                },
              ],
              [
                'OS=="linux"',
                {
                  'cflags_cc' : [
                    '-std=c++11'
                  ],
                  'cflags_cc!': [
                    '-fno-rtti'
                  ]
                }
              ],
              [
                'OS=="mac"',
                {
                  'xcode_settings': {
                    'MACOSX_DEPLOYMENT_TARGET': '10.11',
                    'GCC_ENABLE_CPP_RTTI': 'YES',
                    'OTHER_LDFLAGS': [
                      '-L/usr/local/opt/openssl/lib'
                    ],
                    'OTHER_CPLUSPLUSFLAGS': [
                      '-I/usr/local/opt/openssl/include',
                      '-std=c++11'
                    ],
                  },
                }
              ]
            ]
          }
        ]
      ]
    }
  ]
}
