import subprocess

class Plugin:
    name = "Extra Settings"

    author = "WerWolv"

    main_view_html = """
        <html>
            <head>
                <link rel="stylesheet" href="/steam_resource/css/2.css">
                <link rel="stylesheet" href="/steam_resource/css/39.css">
                <link rel="stylesheet" href="/steam_resource/css/library.css">

                <script>

                    function setToggleState(id, state) {
                        const ENABLED_CLASS = "basicdialog_On_1RyF_";
                        let toggle = document.getElementById(id);

                        if (state && !toggle.classList.contains(ENABLED_CLASS)) {
                            toggle.classList.add(ENABLED_CLASS);
                        }

                        if (!state && toggle.classList.contains(ENABLED_CLASS)) {
                            toggle.classList.remove(ENABLED_CLASS);
                        }
                    }

                    function handleSSHToggle() {
                        let toggle = document.getElementById("sshToggle");

                        let isActive = toggle.classList.contains("basicdialog_On_1RyF_");

                        if (isActive) {
                            call_plugin_method("set_ssh_state", { "state": false }).then((value) => {
                                setToggleState("sshToggle", value);
                            })
                        }
                        else {
                            call_plugin_method("set_ssh_state", { "state": true }).then((value) => {
                                setToggleState("sshToggle", value);
                            })
                        }
                    }

                    async function handleInitialValue() {
                        console.log("InitialValue")
                        let state = await call_plugin_method("get_ssh_state", {});
                        console.log(state)
                        setToggleState("sshToggle", state)
                    }

                </script>
            </head>
            <body onload="handleInitialValue()">
                

                <div class="quickaccessmenu_TabGroupPanel_1QO7b Panel Focusable">
                    <div class="quickaccesscontrols_PanelSectionRow_26R5w">
                        <div class="quickaccesscontrols_PanelSectionRow_26R5w">
                            <div class="basicdialog_Field_ugL9c basicdialog_WithFirstRow_31BpU basicdialog_WithBottomSeparator_1e8sp basicdialog_ExtraPaddingOnChildrenBelow_2-owv basicdialog_StandardPadding_1HrfN basicdialog_HighlightOnFocus_1xh2W Panel Focusable" style="--indent-level:0;">
                                <div class="basicdialog_FieldLabelRow_1oXm0">
                                    <div class="basicdialog_FieldLabel_2URP7">
                                        <div class="basicdialog_FieldLeadIcon_1WR7O">
                                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-server" viewBox="0 0 16 16">
                                            <path d="M1.333 2.667C1.333 1.194 4.318 0 8 0s6.667 1.194 6.667 2.667V4c0 1.473-2.985 2.667-6.667 2.667S1.333 5.473 1.333 4V2.667z"/>
                                            <path d="M1.333 6.334v3C1.333 10.805 4.318 12 8 12s6.667-1.194 6.667-2.667V6.334a6.51 6.51 0 0 1-1.458.79C11.81 7.684 9.967 8 8 8c-1.966 0-3.809-.317-5.208-.876a6.508 6.508 0 0 1-1.458-.79z"/>
                                            <path d="M14.667 11.668a6.51 6.51 0 0 1-1.458.789c-1.4.56-3.242.876-5.21.876-1.966 0-3.809-.316-5.208-.876a6.51 6.51 0 0 1-1.458-.79v1.666C1.333 14.806 4.318 16 8 16s6.667-1.194 6.667-2.667v-1.665z"/>
                                            </svg>
                                        </div>
                                        SSH Server
                                    </div>
                                    <div class="basicdialog_FieldChildren_279n8">
                                        <div id="sshToggle" tabindex="0" class="basicdialog_Toggle_1DKu7 Focusable" onclick="handleSSHToggle()">
                                            <div class="basicdialog_ToggleRail_3ZEjC"></div>
                                        <div class="basicdialog_ToggleSwitch_wXGdI"></div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </body>
        </html>
    """

    tile_view_html = ""

    async def get_ssh_state(self):
        return subprocess.Popen("systemctl is-active sshd", stdout=subprocess.PIPE, shell=True).communicate()[0] == b'active\n'

    async def set_ssh_state(self, **kwargs):
        print(kwargs["state"])

        if kwargs["state"]:
            print(subprocess.Popen("systemctl start sshd", stdout=subprocess.PIPE, shell=True).communicate())
        else:
            print(subprocess.Popen("systemctl stop sshd", stdout=subprocess.PIPE, shell=True).communicate())
        
        return await self.get_ssh_state(self)
