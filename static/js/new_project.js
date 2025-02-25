document.addEventListener('DOMContentLoaded', function() {
    // プロジェクト名入力フィールドのイベントリスナー
    document.getElementById('project_nameInput').addEventListener('input', function(event) {
        document.querySelector('.project_title').innerText = event.target.value;
    });

    // 目標金額入力フィールドのイベントリスナー
    document.getElementById('goalAmountInput').addEventListener('input', function(event) {
        document.getElementById('goalAmount').innerHTML = `<i class="fa-solid fa-yen-sign"></i>${event.target.value}`;
    });

    // 終了日入力フィールドのイベントリスナー
    document.getElementById('endDateInput').addEventListener('input', function(event) {

        const endDate = new Date(event.target.value);
        const today = new Date();
        const timeDiff = endDate - today;
        const daysRemaining = Math.ceil(timeDiff / (1000 * 60 * 60 * 24));

        document.getElementById('endDate').innerText = `${daysRemaining}日`;
    });

    // トップ画像入力フィールドのイベントリスナー
    document.getElementById('top_imgInput').addEventListener('change', function(event) {
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById('topImage').src = e.target.result;
        };
        reader.readAsDataURL(event.target.files[0]);
    });

    // 全てのサブ画像入力フィールドにイベントリスナーを追加
    document.querySelectorAll('.sub_imgInput').forEach((input, index) => {
        input.addEventListener('change', function(event) {
            const reader = new FileReader();
            reader.onload = function(e) {
                document.querySelectorAll('.subImage')[index].src = e.target.result;
            };
            reader.readAsDataURL(event.target.files[0]);
        });
    });

    const project_detail = document.querySelector(".project_detail");
    var detail_count = 0;
    document.getElementById("add_text").addEventListener("click", function() {

        var new_textarea = document.createElement("textarea");
        new_textarea.name = `project_detail-${detail_count}`;
        new_textarea.id = "project_detail";
        project_detail.appendChild(new_textarea)
        detail_count++;
    })

    document.getElementById("add_img").addEventListener("click", function() {
        var new_img = document.createElement("input");
        new_img.type = "file";
        new_img.id = "detail_img";
        new_img.name = `project_detail-${detail_count}`;

        project_detail.appendChild(new_img);

        detail_count++;
    })

    var return_count = 1;
    const return_content = document.getElementById("return");

    document.getElementById("return_add_button").addEventListener("click", function() {
        var return_price = document.createElement("input");
        return_price.type = "number";
        return_price.name = `return_price-${return_count}`;
        var return_textarea = document.createElement("textarea");
        return_textarea.name = `return_textarea-${return_count}`;
        var return_img = document.createElement("input");
        return_img.type = "file";
        return_img.name = `return_img-${return_count}`

        return_content.appendChild(return_price);
        return_content.appendChild(return_textarea);
        return_content.appendChild(return_img);

        return_count++;
    })

    document.getElementById("next_button").addEventListener("click",function() {
        document.getElementById("new_project").style.display = "none";
        document.querySelector(".img_section").style.display = "none";
        document.getElementById("preview_title").style.display = "none";
        document.getElementById("return_section").style.display = "block";
        document.getElementById("submit").style.display = "block";
        document.getElementById("next_button").style.display = "none"
    })

});
