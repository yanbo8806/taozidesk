Name:       taoziapp
Version:    1.1.9
Release:    0
Summary:    RPM package
License:    GPL-3.0
Requires:   gtk3 libxcb1 xdotool libXfixes3 alsa-utils libXtst6 libva2 pam gstreamer-plugins-base gstreamer-plugin-pipewire
Recommends: libayatana-appindicator3-1

# https://docs.fedoraproject.org/en-US/packaging-guidelines/Scriptlets/

%description
The best open-source remote desktop client software, written in Rust.

%prep
# we have no source, so nothing here

%build
# we have no source, so nothing here

%global __python %{__python3}

%install
mkdir -p %{buildroot}/usr/bin/
mkdir -p %{buildroot}/usr/share/taoziapp/
mkdir -p %{buildroot}/usr/share/taoziapp/files/
mkdir -p %{buildroot}/usr/share/icons/hicolor/256x256/apps/
mkdir -p %{buildroot}/usr/share/icons/hicolor/scalable/apps/
install -m 755 $HBB/target/release/taoziapp %{buildroot}/usr/bin/taoziapp
install $HBB/libsciter-gtk.so %{buildroot}/usr/share/taoziapp/libsciter-gtk.so
install $HBB/res/taoziapp.service %{buildroot}/usr/share/taoziapp/files/
install $HBB/res/128x128@2x.png %{buildroot}/usr/share/icons/hicolor/256x256/apps/taoziapp.png
install $HBB/res/scalable.svg %{buildroot}/usr/share/icons/hicolor/scalable/apps/taoziapp.svg
install $HBB/res/taoziapp.desktop %{buildroot}/usr/share/taoziapp/files/
install $HBB/res/taoziapp-link.desktop %{buildroot}/usr/share/taoziapp/files/

%files
/usr/bin/taoziapp
/usr/share/taoziapp/libsciter-gtk.so
/usr/share/taoziapp/files/taoziapp.service
/usr/share/icons/hicolor/256x256/apps/taoziapp.png
/usr/share/icons/hicolor/scalable/apps/taoziapp.svg
/usr/share/taoziapp/files/taoziapp.desktop
/usr/share/taoziapp/files/taoziapp-link.desktop

%changelog
# let's skip this for now

%pre
# can do something for centos7
case "$1" in
  1)
    # for install
  ;;
  2)
    # for upgrade
    systemctl stop taoziapp || true
  ;;
esac

%post
cp /usr/share/taoziapp/files/taoziapp.service /etc/systemd/system/taoziapp.service
cp /usr/share/taoziapp/files/taoziapp.desktop /usr/share/applications/
cp /usr/share/taoziapp/files/taoziapp-link.desktop /usr/share/applications/
systemctl daemon-reload
systemctl enable taoziapp
systemctl start taoziapp
update-desktop-database

%preun
case "$1" in
  0)
    # for uninstall
    systemctl stop taoziapp || true
    systemctl disable taoziapp || true
    rm /etc/systemd/system/taoziapp.service || true
  ;;
  1)
    # for upgrade
  ;;
esac

%postun
case "$1" in
  0)
    # for uninstall
    rm /usr/share/applications/taoziapp.desktop || true
    rm /usr/share/applications/taoziapp-link.desktop || true
    update-desktop-database
  ;;
  1)
    # for upgrade
  ;;
esac
