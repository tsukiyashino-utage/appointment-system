function jump(){
    window.location.href='/logout';
}
$(function(){
    var $users=$('#users');
    var $year=$('#year');
    var $month=$('#month');
    var $day=$('#day');
    var $name=$('#name');

    $('#add-user').on('click',function(){
    
        var user={
            name:$name.val(),
            year: $year.val(),
            month: $month.val(),
            day: $day.val(),
        };

        $.ajax({
            type:'POST',
            url:'/get_panel',
            data:user,
            success: function(user){
                javascript:location.reload();
                alert('提交成功');
            },
            error: function(){
                alert('提交失败');
            }

        });
    });

});