function jump(){
    window.location.href='/logout';
}

$(function(){

    $.ajax({
        type:"GET",
        url:'/get_adminpanel',
        success:function(users){
            $.each(users,function(i,user){
                $('#users').append('<li>用户:'+ user.username +'<br>邮箱:'+ user.email +'<br>预约日期:'+ user.year +'年'+ user.month +'月'+ user.day +'日</li>');
            });
        }
    });

});