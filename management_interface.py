import wx
from person import operate_db
from person import start_interface
import queue


class TreeCtrlFrame(wx.Frame):
    def __init__(self, superior):

        wx.Frame.__init__(self, parent=superior, title='家谱信息管理系统', size=(700, 520))
        image = "management_interface.jpg"
        to_bmp_image = wx.Image(image, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.bitmap = wx.StaticBitmap(self, -1, to_bmp_image, (0, 0))

        self.tree = wx.TreeCtrl(parent=self.bitmap, pos=(5, 5), size=(260, 470))

        # 字体1
        self.font_1 = wx.Font(15, wx.MODERN, wx.NORMAL, wx.NORMAL, False, '隶书')

        # 字体2
        self.font = wx.Font(20, wx.MODERN, wx.NORMAL, wx.NORMAL, False, '隶书')

        # 文本框--姓名
        self.labelName=wx.StaticText(self.bitmap, -1, '姓名', pos=(300,20))
        self.labelName.SetFont(font=self.font)
        self.inputString=wx.TextCtrl(parent=self.bitmap, pos=(370,20), size=(300,30))

        # 性别单选框
        self.labelSex = wx.StaticText(self.bitmap, -1, '性别', pos=(300, 70))
        self.labelSex.SetFont(font=self.font)
        self.radioButtonSexM=wx.RadioButton(self.bitmap, -1, '男', pos=(430, 70), style=wx.RB_GROUP)
        self.radioButtonSexM.SetFont(font=self.font_1)
        self.radioButtonSexF=wx.RadioButton(self.bitmap, -1, '女', pos=(520, 70))
        self.radioButtonSexF.SetFont(font=self.font_1)

        # 文本框--伴侣
        self.labelName = wx.StaticText(self.bitmap, -1, '伴侣', pos=(300, 120))
        self.labelName.SetFont(font=self.font)
        self.inputStringPartner = wx.TextCtrl(parent=self.bitmap, pos=(370, 120))

        # 单选框--是否健在
        self.labelIsLive = wx.StaticText(self.bitmap, -1, '健在', pos=(300, 170))
        self.labelIsLive.SetFont(font=self.font)
        self.radioButtonLive = wx.RadioButton(self.bitmap, -1, '是', pos=(430, 170), style=wx.RB_GROUP)
        self.radioButtonLive.SetFont(font=self.font_1)
        self.radioButtonDie = wx.RadioButton(self.bitmap, -1, '否', pos=(520, 170))
        self.radioButtonDie.SetFont(font=self.font_1)

        # 文本框--出生日期
        self.labelBirthday = wx.StaticText(self.bitmap, -1, '出生\n日期', pos=(300, 220))
        self.labelBirthday.SetFont(font=self.font_1)
        self.inputStringBirthday = wx.TextCtrl(parent=self.bitmap, pos=(370, 220))

        # 选择框--第几代--第几个
        self.labelGeneration = wx.StaticText(self.bitmap, -1, '辈分', pos=(300, 280))
        self.labelGeneration.SetFont(font=self.font)
        self.genaration = {'1': ['1', '2', '3', '4', '5', '6', '7', '8', '9'],
                           '2': ['1', '2', '3', '4', '5', '6', '7', '8', '9'],
                           '3': ['1', '2', '3', '4', '5', '6', '7', '8', '9'],
                           '4': ['1', '2', '3', '4', '5', '6', '7', '8', '9'],
                           '5': ['1', '2', '3', '4', '5', '6', '7', '8', '9'],
                           '6': ['1', '2', '3', '4', '5', '6', '7', '8', '9'],
                           '7': ['1', '2', '3', '4', '5', '6', '7', '8', '9'],
                           '8': ['1', '2', '3', '4', '5', '6', '7', '8', '9'],
                           }

        self.comboBox1 = wx.ComboBox(self.bitmap, value='选择第几代', choices=list(self.genaration.keys()),pos=(370, 280), size=(100,50))
        self.Bind(wx.EVT_COMBOBOX, self.on_combo1, self.comboBox1)
        self.comboBox2 = wx.ComboBox(self.bitmap, value='第几个孩子', choices=[], pos=(500,280), size=(100,50))
        self.Bind(wx.EVT_COMBOBOX, self.on_combo2, self.comboBox2)

        # 添加子节点
        self.buttonAddChild=wx.Button(parent=self.bitmap, label='添加子节点', pos=(300, 330), size=(80, 45))
        self.Bind(wx.EVT_BUTTON, self.on_button_add_child, self.buttonAddChild)

        # 清空历史信息
        self.buttonDeleteNode=wx.Button(parent=self.bitmap, label='删除分支', pos=(410,330), size=(80, 45))
        self.Bind(wx.EVT_BUTTON, self.on_button_delete_node, self.buttonDeleteNode)

        # 添加根节点
        self.buttonAddRoot=wx.Button(parent=self.bitmap, label='添加根节点', pos=(300, 380), size=(80, 45))
        self.Bind(wx.EVT_BUTTON, self.on_button_add_root, self.buttonAddRoot)

        # 家族成员信息查询
        self.buttonMsgSearch = wx.Button(parent=self.bitmap, label='查询家族成员', pos=(410, 380), size=(80, 45))
        self.Bind(wx.EVT_BUTTON, self.on_button_msg_search, self.buttonMsgSearch)

        # 查询近亲
        self.buttonMsgSearchFather= wx.Button(parent=self.bitmap, label='查询近亲', pos=(520, 330), size=(80, 45))
        self.Bind(wx.EVT_BUTTON, self.on_button_msg_search_father, self.buttonMsgSearchFather)

        # 修改信息
        self.buttonUpdate= wx.Button(parent=self.bitmap, label='修改信息\n(健在和伴侣)', pos=(520, 380), size=(80, 45))
        self.Bind(wx.EVT_BUTTON, self.on_button_update, self.buttonUpdate)

        # 查询个人详细信息
        self.button_person_information = wx.Button(parent=self.bitmap, label='查询个人\n详细信息', pos=(300, 430), size=(80, 45))
        self.Bind(wx.EVT_BUTTON, self.on_button_person_information, self.button_person_information)

        # 查询第几代人
        self.button_brother = wx.Button(parent=self.bitmap, label='查询同代人', pos=(410, 430), size=(80, 45))
        self.Bind(wx.EVT_BUTTON, self.on_button_brother, self.button_brother)

        # 帮助
        self.button_help = wx.Button(parent=self.bitmap, label='帮助', pos=(520, 430), size=(80, 45))
        self.Bind(wx.EVT_BUTTON, self.on_button_help, self.button_help)
        self.tree.DeleteAllItems()
        self.init_information()

    # 初始化treectrl控件
    def init_information(self):
        self.tree.DeleteAllItems()
        name = operate_db.select_name_form_cid("1")
        if name:
            q1 = queue.Queue()
            root = self.tree.AddRoot(name)

            # 选中该节点
            self.tree.SelectItem(root, True)
            y = self.tree.GetSelection()

            son_list = operate_db.select_son_name(name)
            for son in son_list:
                q1.put(son)
                x = self.tree.AppendItem(y, son)
                q1.put(x)
            self.tree.SelectItem(root, False)

            while not q1.empty():
                father = q1.get()
                if not self.tree.GetRootItem():
                    pass
                else:

                    son_list = operate_db.select_son_name(father)
                    item_son = q1.get()
                    if type(item_son) is str:
                        pass
                    else:
                        self.tree.SelectItem(item_son, True)
                        y1 = self.tree.GetSelection()
                        for son in son_list:
                            q1.put(son)
                            x_son = self.tree.AppendItem(y1, son)
                            q1.put(x_son)
        else:
            pass


    # 获取姓名输入框中的值
    def get_name(self):
        self.item_string = self.inputString.GetValue()
        return self.item_string

    # 获取单选框中性别的值
    def get_sex(self):
        if self.radioButtonSexM.GetValue():
            self.sex = "男"
        elif self.radioButtonSexF.GetValue():
            self.sex = "女"
        return self.sex

    # 获取出生日期
    def get_birthday(self):
        self.birthday = self.inputStringBirthday.GetValue()
        return self.birthday

    # 获取父亲姓名（当前选中节点的值）
    def get_father(self):
        self.father = self.tree.GetSelection()
        return self.father

    # 获取伴侣框中的值
    def get_partner(self):
        self.partner = self.inputStringPartner.GetValue()
        return self.partner

    # 获取健在单选框的值
    def get_alive(self):
        if self.radioButtonLive.GetValue():
            self.alive = "yes"
        elif self.radioButtonDie.GetValue():
            self.alive = "no"
        return self.alive

    # 获取层级编号
    def get_cid(self, father):

        # 查询父亲的层级编号
        self.f_cid = operate_db.select_person_cid(father)
        # self.choice = self.comboBox1.GetValue()

        # 获得他是父亲的第几个儿子
        self.num = self.comboBox2.GetValue()

        # 父亲的层级编号加上自己的排行号
        self.cid = self.f_cid + str(self.num)
        return self.cid

    # 第一个下拉框的值
    def on_combo1(self, event):
        choice = self.comboBox1.GetValue()
        self.comboBox2.Set(self.genaration[choice])

    # 第二个下拉框
    def on_combo2(self, event):
        wx.MessageBox('确定添加选中人的第'+self.comboBox2.GetValue()+'个孩子？\n\n请单击添加子节点按钮！！！')

    # 添加子节点
    def on_button_add_child(self, event):

        # 判断是否选中父节点
        item_selected=self.tree.GetSelection()
        if not item_selected:
            wx.MessageBox('请先选择父节点')
            return
        else:
            item_selected = self.tree.GetSelection()
            f_name = self.tree.GetItemText(item_selected)
            f_sex = operate_db.select_sex(f_name)

            # 判断所选节点是否为女，性别为女不能作为父节点
            if f_sex == "女":
                wx.MessageBox("此节点性别为女，不可插入子节点")
                return
            else:

                # 判断要插入的名字是否已经存在，若存在不能插入
                name = self.get_name()
                if not name:
                    wx.MessageBox("姓名不能为空!!!")
                    return
                else:
                    flag = operate_db.select_name_insert(name)
                    if flag:
                        wx.MessageBox("该名字已存在，不可插入")
                        return
                    else:
                        sex = self.get_sex()
                        birthday = self.get_birthday()
                        if not birthday:
                            wx.MessageBox("出生日期不能为空！！！")
                            return
                        else:
                            father = self.tree.GetSelection()
                            father = self.tree.GetItemText(father)
                            partner = self.get_partner()
                            if not partner:
                                partner = "暂无"
                            alive = self.get_alive()

                            # 判断层级编号是否重复，若重复拒绝插入
                            cid = self.get_cid(father)
                            flag_cid = operate_db.select_cid(cid)
                            if flag_cid:
                                wx.MessageBox("该辈分的人已存在！！！")
                                return
                            operate_db.insert_zi(name, sex, birthday, father, partner, alive, cid)

                            self.tree.AppendItem(item_selected,name)

    # 删除树形结构，清空数据表中信息
    def on_button_delete_node(self, event):

        name = self.get_name()
        flag = operate_db.select_name_insert(name)
        if flag:
            cid = operate_db.select_person_cid(name)
            new_cid = str(cid) + '%'
            delete_flag = operate_db.delete_son_node(new_cid)
            self.init_information()
            if delete_flag:
                wx.MessageBox("删除该分支成功")
        else:
            wx.MessageBox("您要删除的人不存在！！！")

    # 添加根节点
    def on_button_add_root(self, event):

        # 判断根是否存在
        root_item = self.tree.GetRootItem()
        if root_item:
            wx.MessageBox('第一代已存在！！！')
        else:

            item_string = self.inputString.GetValue()
            name = self.get_name()
            if not name:
                wx.MessageBox("姓名不能为空！！！")
                return
            else:
                sex = self.get_sex()
                birthday = self.get_birthday()
                if not birthday:
                    wx.MessageBox("出生日期不能为空！！！")
                    return
                else:
                    father = None
                    partner = self.get_partner()
                    if not partner:
                        partner = "暂无"
                    alive = self.get_alive()
                    cid = "1"
                    # 判断根是否存在
                    flag_cid = operate_db.select_cid(cid)
                    if flag_cid:
                        wx.MessageBox("第一代已存在！！！")
                        return
                    self.tree.AddRoot(item_string)
                    operate_db.insert_zi(name, sex, birthday, father, partner, alive, cid)

    # 查询家族所有人员的信息
    def on_button_msg_search(self, event):
        list_all = operate_db.select_all()
        start_interface.information_interface(list_all)

    # 查询近亲的姓名
    def on_button_msg_search_father(self, event):
        name = self.get_name()
        if not name:
            wx.MessageBox("查询的姓名不能为空！！！")
            return
        else:
            flag = operate_db.select_name_insert(name)
            if flag:
                list_son = operate_db.select_son_name(name)
                father = operate_db.select_father(name)
                partner = operate_db.select_partner(name)
                wx.MessageBox(name + "的近亲：\n 父亲：%s" % father + "\n儿子：%s" % list_son + "\n伴侣:%s" % partner)
            else:
                wx.MessageBox("您查询的人不存在！！！")

    # 修改伴侣信息和健在状态
    def on_button_update(self, event):
        name = self.get_name()
        if not name:
            wx.MessageBox("姓名不能为空！！！")
            return
        else:
            flag = operate_db.select_name_insert(name)
            if flag:
                partner = self.get_partner()
                alive = self.get_alive()
                operate_db.update_person_partner(name, partner)
                operate_db.update_person_alive(name,alive)

                wx.MessageBox("信息修改成功")
            else:
                wx.MessageBox("您查询的人不存在！！！")

    # 查询个人的详细信息
    def on_button_person_information(self,event):
        name = self.get_name()
        if not name:
            wx.MessageBox("姓名不能为空！！！")
            return
        else:
            flag = operate_db.select_name_insert(name)
            if flag:
                list_person_infirmation = operate_db.select_person(name)
                wx.MessageBox(name + "的详细信息：\n姓名    性别    出生日期    父亲    伴侣  健在   层次编号\n%s" % list_person_infirmation)
            else:
                wx.MessageBox("您查询的人不存在！！！")

    # 查询同一代人
    def on_button_brother(self, event):
        num = self.comboBox1.GetValue()
        if num == '选择第几代':
            wx.MessageBox("尚未选择查询哪一代")
        else:
            cid = int(num) * "_"
            list_brother = operate_db.select_brother(cid)
            wx.MessageBox("第" + num + "代:\n %s " % list_brother)

    # 关于信息
    def on_button_help(self, event):
        str_help =\
            """ 帮助：\n
            1.在开始界面上任意处点击继续，进入家谱管理界面
            2.家谱管理界面，中分为树形结构显示框、信息填入文本框、
               信息选择单选框、信息选择下拉框和操作按钮
            3.添加信息时必须填写项：姓名、出生日期
               默认值：
                性别---->男
                伴侣---->暂无
                健在---->yes
            4.对界面中各个操作按钮进行说明：
            （1）添加子节点：须在左侧的树形结构显示图中选中父节点
            （2）添加根节点：
            （3）查询个人详细信息：必须在姓名一栏填写要查询的姓名
            （4）删除分支：必须在姓名一栏填写要删除分支的人的姓名
            （5）查询家族成员：
            （6）查询同代人：必须在辈分的第一个下拉框中选择第几代
            （7）查询近亲：必须在姓名一栏填写要查询的姓名
            （8）修改信息：必须在姓名一栏填写要查询的姓名，
                            在伴侣一栏填写要更改的姓名或选择健在状态
            （9）帮助：显示本系统的帮助
                                                             本系统开发人员：SQX, ZXP, LB
    """
        wx.MessageBox(str_help)


if __name__=='__main__':
    app = wx.App()
    frame = TreeCtrlFrame(None)
    frame.Show()
    app.MainLoop()
