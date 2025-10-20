{ pkgs }: {
  deps = [
    pkgs.python310Full
    pkgs.python310Packages.pip
    pkgs.postgresql
    pkgs.gcc
    pkgs.zlib
  ];
  
  env = {
    PYTHON_LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
      pkgs.stdenv.cc.cc.lib
      pkgs.zlib
    ];
  };
}

