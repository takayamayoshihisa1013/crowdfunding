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

});
