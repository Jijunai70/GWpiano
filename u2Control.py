import os
import time

import uiautomator2 as u2


class ATU:
    def __init__(self):
        try:
            self.d = u2.connect()  # connect to device
        except Exception as e:
            print(f"连接设备失败：{e}")

    def get_element(self, element_id):
        return self.d(resourceId=element_id).get_text()

    def click_element(self, element_id):
        self.d(resourceId=element_id).click()

    def input_text(self, element_id, text):
        self.d(resourceId=element_id).set_text(text)

    def showXML(self):
        # 获取当前界面的 XML 层级结构
        xml_hierarchy = self.d.dump_hierarchy()
        print(xml_hierarchy)

    def click(self, x, y):
        self.d.click(x, y)

    def sendKey(self, text):
        self.d.send_keys(text)

def click_multiple_spots(coordinates):
    command = " & ".join([f"adb shell input tap {x} {y}" for x, y in coordinates])
    os.system(command)


# 调用函数点击多个地方
click_multiple_spots([(761, 343)])

atu = ATU()
atu.click(100, 100)

# root 600+30+10, 61+30+10 640, 100
# 每格偏移宽131 高122
# 600-761 61-214 宽161 高153px
# 762-893 61-214 宽131 高153px
# 894-1026 61-214 宽132 高153px
# 600-761 215-342 宽161 高127px
# 600-761 343-495 宽161 高122px

atu.click(640, 100)
atu.click(771, 100)
atu.click(902, 100)
atu.click(1033, 100)
atu.click(1164, 100)
atu.click(640, 222)
atu.click(771, 222)
atu.click(902, 222)
atu.click(1033, 222)
atu.click(1164, 222)
atu.click(640, 344)
atu.click(771, 344)
atu.click(902, 344)
atu.click(1033, 344)
atu.click(1164, 344)


root = (640, 100)
for i in range(3):
    for j in range(5):
        x = root[0] + j * 131
        y = root[1] + i * 122
        atu.click(x, y)
        print("atu.click({}, {})".format(x, y))
        time.sleep(0.1)
