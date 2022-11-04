$(".comment_reply_btn").click(function (event) {
    event.preventDefault();
    $(this).next('.reply_comment_block').find('.reply_jquery_block').fadeToggle();
});
