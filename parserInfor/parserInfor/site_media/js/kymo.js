    function shareClick() {
        var rrShareParam = {
            resourceUrl : '',   //分享的资源Url
            srcUrl : '',    //分享的资源来源Url,默认为header中的Referer,如果分享失败可以调整此值为resourceUrl试试
            pic : '',       //分享的主题图片Url
            title : '',     //分享的标题
            description : ''    //分享的详细描述
    };
    rrShareOnclick(rrShareParam);
    }
