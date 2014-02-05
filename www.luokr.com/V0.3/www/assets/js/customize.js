// Global namespace
window.Luokr = window.Luokr || {};
Luokr.Global = Luokr.Global || {};
Luokr.Module = Luokr.Module || {};

Luokr.Global.config = Luokr.Global.config || {};
Luokr.Global.method = Luokr.Global.method || {};
Luokr.Global.source = Luokr.Global.source || {};
Luokr.Global.string = Luokr.Global.string || {};

Luokr.Global.string.SUCCESS = '操作成功！';
Luokr.Global.string.FAILURE = '操作失败！';
Luokr.Global.string.WAITING = '处理中，请稍侯...';
Luokr.Global.string.LOADING = '加载中，请稍侯...';
Luokr.Global.string.POSTING = '发送中，请稍侯...';
Luokr.Global.string.CONFIRM = '确认执行该操作吗？';

/**
* Format date time
* @param string a Format
* @param int    s Timestamp
*/
Luokr.Global.method.date = function(a, s)
{
    var d = s ? new Date(s) : new Date(), f = d.getTime();
    return ('' + a).replace(/a|A|d|D|F|g|G|h|H|i|I|j|l|L|m|M|n|s|S|t|T|U|w|y|Y|z|Z/g, function(a) {
        switch (a) {
        case 'a' : return d.getHours() > 11 ? 'pm' : 'am';  
        case 'A' : return d.getHours() > 11 ? 'PM' : 'AM';  
        case 'd' : return ('0' + d.getDate()).slice(-2);  
        case 'D' : return ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'][d.getDay()];  
        case 'F' : return ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'][d.getMonth()];  
        case 'g' : return (s = (d.getHours() || 12)) > 12 ? s - 12 : s;  
        case 'G' : return d.getHours();  
        case 'h' : return ('0' + ((s = d.getHours() || 12) > 12 ? s - 12 : s)).slice(-2);  
        case 'H' : return ('0' + d.getHours()).slice(-2);  
        case 'i' : return ('0' + d.getMinutes()).slice(-2);  
        case 'I' : return (function(){d.setDate(1); d.setMonth(0); s = [d.getTimezoneOffset()]; d.setMonth(6); s[1] = d.getTimezoneOffset(); d.setTime(f); return s[0] == s[1] ? 0 : 1;})();  
        case 'j' : return d.getDate();  
        case 'l' : return ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'][d.getDay()];  
        case 'L' : return (s = d.getFullYear()) % 4 == 0 && (s % 100 != 0 || s % 400 == 0) ? 1 : 0;  
        case 'm' : return ('0' + (d.getMonth() + 1)).slice(-2);  
        case 'M' : return ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][d.getMonth()];  
        case 'n' : return d.getMonth() + 1;  
        case 's' : return ('0' + d.getSeconds()).slice(-2);  
        case 'S' : return ['th', 'st', 'nd', 'rd'][(s = d.getDate()) < 4 ? s : 0];  
        case 't' : return (function(){d.setDate(32); s = 32 - d.getDate(); d.setTime(f); return s;})();  
        case 'T' : return 'UTC';  
        case 'U' : return ('' + f).slice(0, -3);  
        case 'w' : return d.getDay();  
        case 'y' : return ('' + d.getFullYear()).slice(-2);  
        case 'Y' : return d.getFullYear();  
        case 'z' : return (function(){d.setMonth(0); return d.setTime(f - d.setDate(1)) / 86400000;})();  
        default  : return -d.getTimezoneOffset() * 60;  
        };  
    });  
};  


Luokr.Global.method.confirm = function(options)
{
    return confirm(Luokr.Global.string.CONFIRM);
}

Luokr.Global.method.prepare = function(options)
{
    var setting = {
        message: Luokr.Global.string.WAITING
    };
    $.extend(setting, options || {});

    easyDialog.open({
        container : {content: '<div class="ajax-form-loading"></div><p class="text-center">' + setting.message + '</p>'},
        drag : false
    });
}

Luokr.Global.method.request = function(options)
{
    var setting = {
        element: null,
        forward: true,

        prepare: Luokr.Global.method.prepare,
        success: Luokr.Global.method.respond,
        failure: null  // *Unsupported!
    };

    if (options && !options.element) {
        setting.element = options;
    } else {
        $.extend(setting, options || {});
    }

    if (!setting.element) {
        return false;
    }

    setting.element = $(setting.element);

    if (setting.element.is('form')) {
        var form = setting.element;
        // if (!form.valid()) {
        //     return false;
        // }

        $.ajax({
            url       : form.attr('action'),
            type      : form.attr('method'),
            data      : form.serialize(),
            dataType  : 'json',
            beforeSend: function(){
                setting.prepare(setting);
            },
            success   : function(respond){
                setting.success(setting, respond);

                if (window.Recaptcha && $('#recaptcha').length) {
                    Recaptcha.reload()
                }
            }
        });
    } else {
        var link = setting.element;

        $.ajax({
            url       : link.attr('href') || link.attr('alt'),
            type      : 'get',
            dataType  : 'json',
            beforeSend: function(){
                setting.prepare(setting);
            },
            success   : function(respond){
                setting.success(setting, respond);
            }
        });
    }

    return false;
}

Luokr.Global.method.respond = function(opts, data)
{
    var args = {forward: true};
    $.extend(args, opts || {});

    if (data.err) {
        easyDialog.open({
            container : {
                header : Luokr.Global.string.FAILURE,
                content : '<div style="color:red">' + (data.msg == null || data.msg == '' ? Luokr.Global.string.FAILURE : data.msg) + '</div>'
            },
            autoClose : data.url ? (data.tms || 5)*1000 : 0
        });
    } else {
        var msgs = [];
        if (data.msg != null && data.msg != '') {
            msgs.push(data.msg);
        }

        if (args.forward || data.url) {
            if (data.url == '') {
                msgs.push('继续操作，请 <a href="javascript:location.reload()">刷新当前页</a> 或 <a href="javascript:history.go(-1)">返回上一页</a>');
            } else {
                setTimeout(function(){location.href = data.url;}, (data.tms || 3)*1000);
            }
        } else {
            setTimeout(function(){easyDialog.close()}, (data.tms || 3)*1000);
        }

        easyDialog.open({
            container : {
                header: Luokr.Global.string.SUCCESS,
                content : ('<div>' + (msgs.length ? msgs.join('<br/>') : Luokr.Global.string.SUCCESS) + '</div>')
            }
        });
    }
}

Luokr.Global.method.ajaxForm = function(form, stay)
{
    if (window.CKEDITOR)
    {
        for (instance in CKEDITOR.instances)
        {
            CKEDITOR.instances[instance].updateElement();
        }
    }

    Luokr.Global.method.request({element: form, forward: !stay});
    return false;
};

Luokr.Global.method.ajaxLink = function(link, stay)
{
    Luokr.Global.method.request({element: link, forward: !stay});
    return false;
};

$(function(){
    if ($('body').data('exts-scrollup'))
    {
        $.scrollUp({
            scrollName: 'scrollUp', // Element ID
            topDistance: '300', // Distance from top before showing element (px)
            topSpeed: 300, // Speed back to top (ms)
            animation: 'fade', // Fade, slide, none
            animationInSpeed: 200, // Animation in speed (ms)
            animationOutSpeed: 200, // Animation out speed (ms)
            scrollText: '', // Text for element
            activeOverlay: false  // Set CSS color to display scrollUp active point, e.g '#00FFFF'
        });
    }

    $('.require-confirm').on('click', function(){
        return Luokr.Global.method.confirm();
    });

    $('.request-ajax-link-with-confirm').on('click', function(){
        if (Luokr.Global.method.confirm())
        {
            Luokr.Global.method.ajaxLink($(this));
        }
        return false;
    });

    $('.request-ajax-link').on('click', function(){
        Luokr.Global.method.ajaxLink($(this));
        return false;
    });

    $('.request-ajax-form-with-confirm').on('submit', function(){
        if (Luokr.Global.method.confirm())
        {
            Luokr.Global.method.ajaxForm($(this));
        }
        return false;
    });

    $('.request-ajax-form').on('submit', function(){
        Luokr.Global.method.ajaxForm($(this));
        return false;
    });
});
