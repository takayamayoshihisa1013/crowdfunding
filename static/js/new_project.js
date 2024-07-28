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
});
