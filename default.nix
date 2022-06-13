{
  pkgs ? import (fetchTarball "https://github.com/NixOS/nixpkgs/archive/nixos-22.05.tar.gz") {},
}:

let

  inherit (pkgs) lib python3Packages;
  inherit (pkgs) gtk3 gobject-introspection libappindicator-gtk3 wrapGAppsHook;
  inherit (python3Packages) python buildPythonApplication fetchPypi;

in buildPythonApplication rec {
  pname = "bttray";
  version = "0.0.1";
  namePrefix = "";

  src = ./.;

  buildInputs = [
    gtk3
    gobject-introspection
  ];

  nativeBuildInputs = [
    wrapGAppsHook
  ];

  propagatedBuildInputs = with python3Packages; [
    pygobject3
    libappindicator-gtk3
    pulsectl
  ];

  doCheck = false; # no tests

  meta = {
    description = "Simple tray icon to swap Bluetooth headset modes";
    license = lib.licenses.mit;
    maintainers = with lib.maintainers; [ andrew-d ];
    platforms = lib.platforms.linux;
  };
}
