document.addEventListener('DOMContentLoaded', () => {
    console.log('loaded...');
    try {
        document.querySelector('#folunfol').addEventListener('click', followHandler)
    } catch (error) {
        console.log(error);
    }
    document.querySelectorAll('.edit').forEach(button => {
        button.addEventListener('click', editHandler)
    })
    console.log(document.querySelectorAll('.actions'));
    document.querySelectorAll('.actions').forEach(action => {
        action.addEventListener('click', likesHandler)
    });

})

function getCookie(name) {
    if (!document.cookie) {
      return null;
    }

    const xsrfCookies = document.cookie.split(';')
      .map(c => c.trim())
      .filter(c => c.startsWith(name + '='));

    if (xsrfCookies.length === 0) {
      return null;
    }
    return decodeURIComponent(xsrfCookies[0].split('=')[1]);
}

const csrfToken = getCookie('CSRF-TOKEN');

const headers = new Headers({
        'Content-Type': 'x-www-form-urlencoded',
        'X-CSRF-TOKEN': csrfToken
});

// The following function are copying from
// https://docs.djangoproject.com/en/dev/ref/csrf/#ajax
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const followHandler = (e) => {
    let userStatus = e.target.value.toLowerCase()
    let data = {
        following: document.querySelector('#target').innerHTML,
        status: userStatus
    }

    let csrftoken = getCookie('csrftoken');
    fetch("/follow", {
        method: 'POST',
        body: JSON.stringify(data),
        headers: { "X-CSRFToken": csrftoken },
    }).then(response => response.json())
    .then(result => {
        const follower = document.querySelector('#follower')
        console.log(result['followers']);
        follower.innerHTML = result['followers'].toString()
        if (userStatus==="1"){
            e.target.innerHTML = "Follow"
            e.target.value = "0"
        } else {
            e.target.innerHTML = "Unfollow"
            e.target.value = "1"
        }
    })
}

const editHandler = (e) => {
    const id = e.target.value

    if (e.target.innerHTML === 'edit') {
        document.querySelector(`.textarea-${id}`).style.display = 'block'
        document.querySelector(`.date-${id}`).style.display = 'none'
        document.querySelector(`.content-${id}`).style.display = 'none'
        e.target.innerHTML = 'save'
    } else {
        console.log(document.querySelector(`.textarea-${id}`).value);
        data = {
            data: document.querySelector(`.textarea-${id}`).value
        }
        let csrftoken = getCookie('csrftoken');
        fetch(`/post/${id}`, {
            method: 'POST',
            body: JSON.stringify(data),
            headers: { "X-CSRFToken": csrftoken },
        })
        .then(response => response.json())
        .then(res => {
            document.querySelector(`.textarea-${id}`).style.display = 'none'

            const dateField = document.querySelector(`.date-${id}`)
            const contentField = document.querySelector(`.content-${id}`)

            e.target.innerHTML = 'edit'
            console.log(res)
            contentField.innerHTML = res.post.post
            dateField.innerHTML = formatDate(res.post.date)
            dateField.style.display = 'block'
            contentField.style.display = 'block'


        })


    }
}


const MONTH_TO_ALPHA = {
    '01': 'Jan',
    '02': 'Feb',
    '03': 'Mar',
    '04': 'Apr',
    '05': 'May',
    '06': 'Jun',
    '07': 'Jul',
    '08': 'Aug',
    '09': 'Sept',
    '10': 'Oct',
    '11': 'Nov',
    '12': 'Dec'
}

const formatHour = (hour) => {
    hour = parseInt(hour)
    if (hour==12 || hour==24){
        return [12, hour==12?'p.m.':'a.m.']
    }
    return [hour%12, hour<13?'a.m.':'p.m.']

}

const formatDate = (date) => {
    const year = date.slice(0, 4)
    const month = MONTH_TO_ALPHA[date.slice(5, 7)]
    const day = date.slice(8, 10)
    const [hour, format] = formatHour(date.slice(11, 13))
    const minute = date.slice(14, 16)

    return `${month}. ${day}, ${year}, ${hour}:${minute} ${format}`
}

const likesHandler = (e) => {
    const id = e.target.id.split('actions-')[1]
    let csrftoken = getCookie('csrftoken');
    if(typeof id !== "undefined") {
        fetch(`/likes/${id}`, {
            method: 'POST',
            headers: { "X-CSRFToken": csrftoken },
        }).then(response => response.json())
        .then(res => {
            e.target.innerHTML = ` ${res['likes']}`
            if (e.target.style.color === "") {
                e.target.style.color = "#b33"
            } else {
                e.target.style.color = ""
            }
        })
    }
}