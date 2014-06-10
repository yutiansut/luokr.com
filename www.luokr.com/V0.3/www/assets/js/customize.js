// Global namespace
window.L = window.L || {};
L.Global = L.Global || {};
L.Module = L.Module || {};

L.Global.config = L.Global.config || {};
L.Global.method = L.Global.method || {};
L.Global.source = L.Global.source || {};
L.Global.string = L.Global.string || {};
L.Global.widget = L.Global.widget || {};

L.Global.string.SUCCESS = '操作成功！';
L.Global.string.FAILURE = '操作失败！';
L.Global.string.WAITING = '处理中，请稍侯...';
L.Global.string.LOADING = '加载中，请稍侯...';
L.Global.string.POSTING = '发送中，请稍侯...';
L.Global.string.CONFIRM = '确认执行该操作吗？';

/**
* Format date time
* @param string a Format
* @param int    s Timestamp
*/
L.Global.method.date = function(a, s)
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


L.Global.method.confirm = function(message)
{
    return confirm(typeof(message) == "undefined" ? L.Global.string.CONFIRM : message);
}

L.Global.method.prepare = function(options)
{
    var setting = {
        message: L.Global.string.WAITING
    };
    $.extend(setting, options || {});

    easyDialog.open({
        container : {content: '<div class="ajax-form-loading"></div><p class="text-center">' + setting.message + '</p>'},
        drag : false
    });
}

L.Global.method.request = function(options)
{
    var setting = {
        element: null,
        forward: true,

        prepare: L.Global.method.prepare,
        success: L.Global.method.respond,
        failure: null  // *Unsupported!
    };

    $.extend(setting, options || {});

    if (!setting.element) {
        if (setting._action) {
            $.ajax({
                url       : setting._action,
                type      : setting._method || 'get',
                data      : setting._params || '',
                dataType  : setting._format || 'json',
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
                L.Global.widget.captcha.reload();
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

L.Global.method.respond = function(opts, data)
{
    var args = {forward: true};
    $.extend(args, opts || {});

    var msgs = [];
    if (data.msg != null && data.msg != '') {
        msgs.push(data.sta ? data.sta + ' ' + data.msg : data.msg);
    }

    if (data.err) {
        if (args.forward && data.url) {
            msgs.push('放弃操作，请 <a href="' + data.url + '">点击这里</a>');
        }

        easyDialog.open({
            container : {
                header : L.Global.string.FAILURE,
                content : '<div style="color:red">' + (msgs.length ? msgs.join('<br/>') : L.Global.string.FAILURE) + '</div>'
            }
        });
    } else {
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
                header: L.Global.string.SUCCESS,
                content : ('<div>' + (msgs.length ? msgs.join('<br/>') : L.Global.string.SUCCESS) + '</div>')
            }
        });
    }
}

L.Global.method.ajaxSend = function(method, action, params, format)
{
    L.Global.method.request({_method: method, _action: action, _params: params, _format: format});
    return false;
};

L.Global.method.ajaxForm = function(form, stay)
{
    if (window.CKEDITOR)
    {
        for (instance in CKEDITOR.instances)
        {
            CKEDITOR.instances[instance].updateElement();
        }
    }

    L.Global.method.request({element: form, forward: !stay});
    return false;
};

L.Global.method.ajaxLink = function(link, stay)
{
    L.Global.method.request({element: link, forward: !stay});
    return false;
};


L.Global.widget.captcha = {};
L.Global.widget.captcha.create = function()
{
    element = $('#recaptcha');
    if (element.html() == '') {
        var tpl = '' +
        '<div id="recaptcha_widget" class="recaptcha-widget recaptcha_isnot_showing_audio">' +
        '    <div id="recaptcha_image"></div>' +
        '    <div class="recaptcha-main">' +
        '        <div class="recaptcha-buttons">' +
        '            <a id="recaptcha_reload_btn" href="javascript:L.Global.widget.captcha.reload(' + "'" + element.selector + "'" + ');" title="获取新的验证"><span>&nbsp;</span></a>' +
        '        </div>' +
        '        <label>' +
        '            <strong>' +
        '                <span id="recaptcha_instructions_image" class="recaptcha_only_if_image">' +
        '                    输入验证码：' +
        '                </span>' +
        '            </strong>' +
        '            <input type="text" id="recaptcha_response_field" name="_code">' +
        '        </label>' +
        '    </div>' +
        '</div>' +
        '';
        
        element.addClass('.captcha').html(tpl);
    }

    $('#recaptcha_image').html('<img class="captcha-image" src="/image/random?' + (new Date).getTime() + '">');
};
L.Global.widget.captcha.reload = function()
{
    $('#recaptcha_image').html('<img class="captcha-image" src="/image/random?' + (new Date).getTime() + '">');
    $('#recaptcha_response_field').select();
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
        return L.Global.method.confirm();
    });

    $('.request-ajax-link-with-confirm').on('click', function(){
        if (L.Global.method.confirm())
        {
            L.Global.method.ajaxLink($(this));
        }
        return false;
    });

    $('.request-ajax-link').on('click', function(){
        L.Global.method.ajaxLink($(this));
        return false;
    });

    $('.request-ajax-form-with-confirm').on('submit', function(){
        if (L.Global.method.confirm())
        {
            L.Global.method.ajaxForm($(this));
        }
        return false;
    });

    $('.request-ajax-form').on('submit', function(){
        L.Global.method.ajaxForm($(this));
        return false;
    });
});
