$(".comment_reply_btn").click(function (event) {
    event.preventDefault();
    $(this).next('.reply_comment_block').find('.reply_jquery_block').fadeToggle();
});

console.log('hello world')
const alertBox = document.getElementById('alert-box')
const imageBox = document.getElementById('image-box')
const imageForm = document.getElementById('image-form')
const confirmBtn = document.getElementById('confirm-btn')
const input = document.getElementById('id_profile_pic')

const csrf = document.getElementsByName('csrfmiddlewaretoken')


input.addEventListener('change', () => {
    alertBox.innerHTML = ""
    confirmBtn.classList.remove('not-visible')
    const img_data = input.files[0]
    const url = URL.createObjectURL(img_data)

    imageBox.innerHTML = `<img src="${url}" id="image" width="200px" alt="profile picture">`
    var $image = $('#image');

    $image.cropper({
        aspectRatio: 9 / 9,
        crop: function (event) {
            console.log(event.detail.x);
            console.log(event.detail.y);
            console.log(event.detail.width);
            console.log(event.detail.height);
            console.log(event.detail.rotate);
            console.log(event.detail.scaleX);
            console.log(event.detail.scaleY);
        }
    });

    var cropper = $image.data('cropper');
    confirmBtn.addEventListener('click', ()=>{
        cropper.getCroppedCanvas().toBlob((blob) => {
            console.log('confirmed')


            $.ajax({
                type:'POST',
                action: imageForm.action,
                enctype: 'multipart/form-data',
                data: imageForm,
                success: function(response){
                    console.log('success', response)
                    alertBox.innerHTML = `<div class="alert alert-success" role="alert">
                                            Successfully saved and cropped the selected image
                                        </div>`
                },
                error: function(error){
                    console.log('error', error)
                    alertBox.innerHTML = `<div class="alert alert-danger" role="alert">
                                            Ups...something went wrong
                                        </div>`
                },
                cache: false,
                contentType: false,
                processData: false,
            })
        })
    })
});


