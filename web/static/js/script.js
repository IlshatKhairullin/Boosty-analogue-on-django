$(".comment_reply_btn").click(function (event) {
    event.preventDefault();
    $(this).next('.reply_comment_block').find('.reply_jquery_block').fadeToggle();
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

console.log('hello world')
const alertBox = document.getElementById('alert-box')
const imageBox = document.getElementById('image-box')
const imageForm = document.getElementById('image-form')
const confirmBtn = document.getElementById('confirm-btn')
const input1 = document.getElementById('id_profile_pic')
const sidebar = document.getElementsByClassName('profile_aside_block')
const back_link = document.getElementById('back_link')
const post_list_button = document.getElementById('post_list_button')

const input2 = document.getElementById('id_profile_background')


input1.addEventListener('change', () => {
    alertBox.innerHTML = ""
    confirmBtn.classList.remove('not-visible')
    back_link.classList.remove('not-visible')
    post_list_button.classList.add('not-visible')

    for (const box of sidebar) {
        box.classList.add('not-visible');
    }

    const img_data = input1.files[0]
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
    confirmBtn.addEventListener('click', () => {
        cropper.getCroppedCanvas().toBlob((blob) => {
            console.log('confirmed')

            const csrftoken = getCookie('csrftoken')

            const fd = new FormData(imageForm);
            fd.append('profile_pic', blob, 'profile_pic.png');

            $.ajax({
                type: 'POST',
                headers: {'X-CSRFToken': csrftoken},
                url: imageForm.action,
                enctype: 'multipart/form-data',
                data: fd,
                success: function (response) {
                    console.log('success', response)
                    alertBox.innerHTML = `<div class="alert alert-success" role="alert">
                                            Successfully saved and cropped the selected image
                                        </div>`
                },
                error: function (error) {
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


input2.addEventListener('change', () => {
    alertBox.innerHTML = ""
    confirmBtn.classList.remove('not-visible')
    back_link.classList.remove('not-visible')
    post_list_button.classList.add('not-visible')

    for (const box of sidebar) {
        box.classList.add('not-visible');
    }

    const img_data = input2.files[0]
    const url = URL.createObjectURL(img_data)

    imageBox.innerHTML = `<img src="${url}" id="image" width="200px" alt="profile picture">`
    var $image = $('#image');

    $image.cropper({
        aspectRatio: 16 / 9,
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
    confirmBtn.addEventListener('click', () => {
        cropper.getCroppedCanvas().toBlob((blob) => {
            console.log('confirmed')

            const csrftoken = getCookie('csrftoken')

            const fd = new FormData(imageForm);
            fd.append('profile_background', blob, 'profile_background.png');

            $.ajax({
                type: 'POST',
                headers: {'X-CSRFToken': csrftoken},
                url: imageForm.action,
                enctype: 'multipart/form-data',
                data: fd,
                success: function (response) {
                    console.log('success', response)
                    alertBox.innerHTML = `<div class="alert alert-success" role="alert">
                                            Successfully saved and cropped the selected image
                                        </div>`
                },
                error: function (error) {
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

