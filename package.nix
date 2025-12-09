{
  pkgs ? import <nixpkgs> {},
  lib ? pkgs.lib,
}:
pkgs.stdenvNoCC.mkDerivation {
  pname = "wpressarc";
  version = "2025-12-09";
  src = ./.;
  buildPhase = ''
    runHook preBuild

    # Patch the shebang for wpressarc
    sed -i '1 s|^.*$|#!${pkgs.python3}/bin/python3|' wpressarc

    runHook postBuild
  '';
  checkInputs = [pkgs.python3];
  checkPhase = ''
    runHook preCheck

    ${pkgs.bash}/bin/bash test.sh

    runHook postCheck
  '';
  doCheck = true;
  installPhase = ''
    runHook preInstall

    mkdir -p $out/bin
    install -m755 wpressarc $out/bin/wpressarc

    runHook postInstall
  '';
  meta = with lib; {
    description = "Convert ai1wm wpress archives to and from tar archives";
    homepage = "https://github.com/kugland/wpressarc";
    license = licenses.mit;
    maintainers = [maintainers.kugland];
    platforms = platforms.all;
    mainProgram = "wpressarc";
  };
}
