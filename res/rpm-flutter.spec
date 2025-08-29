Name:       taoziapp
Version:    1.4.2
Release:    0
Summary:    RPM package
License:    GPL-3.0
URL:        https://taoziapp.com
Vendor:     taoziapp <info@taoziapp.com>
Requires:   gtk3 libxcb libxdo libXfixes alsa-lib libva pam gstreamer1-plugins-base
Recommends: libayatana-appindicator-gtk3
Provides:   libdesktop_drop_plugin.so()(64bit), libdesktop_multi_window_plugin.so()(64bit), libfile_selector_linux_plugin.so()(64bit), libflutter_custom_cursor_plugin.so()(64bit), libflutter_linux_gtk.so()(64bit), libscreen_retriever_plugin.so()(64bit), libtray_manager_plugin.so()(64bit), liburl_launcher_linux_plugin.so()(64bit), libwindow_manager_plugin.so()(64bit), libwindow_size_plugin.so()(64bit), libtexture_rgba_renderer_plugin.so()(64bit)

# https://docs.fedoraproject.org/en-US/packaging-guidelines/Scriptlets/

%description
The best open-source remote desktop client software, written in Rust.

%prep
# we have no source, so nothing here

%build
# we have no source, so nothing here

# %global __python %{__python3}

%install

mkdir -p "%{buildroot}/usr/share/taoziapp" && cp -r ${HBB}/flutter/build/linux/x64/release/bundle/* -t "%{buildroot}/usr/share/taoziapp"
mkdir -p "%{buildroot}/usr/bin"
install -Dm 644 $HBB/res/taoziapp.service -t "%{buildroot}/usr/share/taoziapp/files"
install -Dm 644 $HBB/res/taoziapp.desktop -t "%{buildroot}/usr/share/taoziapp/files"
install -Dm 644 $HBB/res/taoziapp-link.desktop -t "%{buildroot}/usr/share/taoziapp/files"
install -Dm 644 $HBB/res/128x128@2x.png "%{buildroot}/usr/share/icons/hicolor/256x256/apps/taoziapp.png"
install -Dm 644 $HBB/res/scalable.svg "%{buildroot}/usr/share/icons/hicolor/scalable/apps/taoziapp.svg"

%files
/usr/share/taoziapp/*
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
ln -sf /usr/share/taoziapp/taoziapp /usr/bin/taoziapp
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
    rm /usr/bin/taoziapp || true
    rmdir /usr/lib/taoziapp || true
    rmdir /usr/local/taoziapp || true
    rmdir /usr/share/taoziapp || true
    rm /usr/share/applications/taoziapp.desktop || true
    rm /usr/share/applications/taoziapp-link.desktop || true
    update-desktop-database
  ;;
  1)
    # for upgrade
    rmdir /usr/lib/taoziapp || true
    rmdir /usr/local/taoziapp || true
  ;;
esac
