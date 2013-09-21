CKEDITOR.plugins.add(
	"code",
	{
	requires:["dialog"],
	lang:["en"],
	init:function (a)
	{
		a.addCommand("code", new CKEDITOR.dialogCommand("code"));
		a.ui.addButton(
		"Code",
		{
			label:"插入图片",
			command:"code",
			icon:this.path + "code.gif"
		});
		CKEDITOR.dialog.add("code", this.path + "dialogs/code.js");
	}
}
);
