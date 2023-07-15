import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15

ApplicationWindow {
    id: window_root

    Material.theme: Material.Dark
    //Material.accent: ColorTheme.active.color(ColorTheme.Primary)
    //Material.primary: ColorTheme.active.color(ColorTheme.Accent)
    //Material.foreground: ColorTheme.active.color(ColorTheme.Text)
    //Material.background: ColorTheme.active.color(ColorTheme.BaseShade)

    title: "MSysMonitor"
    minimumWidth: 720
    minimumHeight: 360
    width: 1280
    height: 800
    visible: true
    //color: ColorTheme.active.color(ColorTheme.Dark)

    Loader {
        anchors.fill: parent
        active: !splashscreen.enabled
        asynchronous: true

        sourceComponent: Item {
            id: root

            //property string mainfont: font_Main.name
            //property string monofont: font_Mono.name

            anchors.fill: parent
            layer.smooth: true
            layer.samples: 8
            layer.enabled: true

            //FontLoader { id: font_Main; source: "qrc:/fonts/Overpass.ttf" }
            //FontLoader { id: font_Mono; source: "qrc:/fonts/UbuntuMono.ttf" }

        }
    }

    // Widgets.SplashScreen {
    //     id: splashscreen
    //
    //     anchors.fill: parent
    //     enabled: true
    //
    //     Timer {
    //         interval: 800
    //         repeat: false
    //         running: true
    //         onTriggered: splashscreen.enabled = false
    //     }
    //
    // }
}
