

function chk(n){
    var ban = document.getElementById("ban");
    var sub = document.getElementById("sub");
    var submit = document.getElementById("sb");
    if(n==0){
        ban.style.display = 'flex';
        sub.style.display = 'none';
        submit.style.display = 'none';
    }
    if(n==1){
        ban.style.display = 'none';
        sub.style.display = 'flex';
        submit.style.display = 'none';
    }
    if(n==2){
        ban.style.display = 'none';
        sub.style.display = 'none';
        submit.style.display = 'flex';
    }
}

function st(n){
    var yes = document.getElementById("yes");
    var no = document.getElementById("no");
    var submit_div = document.getElementById("submit_div");
    if(n==0){
        yes.style.display = 'none';
        no.style.display = 'flex';
        submit_div.style.display = 'flex';
    }
    if(n==1){
        yes.style.display = 'flex';
        no.style.display = 'none';
        submit_div.style.display = 'none';

    }
}

