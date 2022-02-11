function tors(tors){
    var teacher = document.getElementById("teacher");
    var student = document.getElementById("student");
    var teacher_number=document.getElementById("teacher_number");
    var student_number =document.getElementById('student_number');
    var t =document.getElementById('t');
    var chk = document.getElementById('chk');
    if(tors ==1){
        teacher_number.style.display='flex';
        student_number.style.display='none';
        teacher.style.display='none';
        student.style.display='flex';
        t.style.display='flex';
        chk.value = "1";
    }
    if(tors ==2){
        teacher_number.style.display='none';
        student_number.style.display='flex';
        teacher.style.display='flex';
        student.style.display='none';
        t.style.display='none';
        chk.value = "0";
    }
}

function chk(val){
    document.getElementById(number).value=val;
    alert(document.getElementById(number).value);
}