new Vue({
    el: '#chat_list_app',
    data: {
        chats: [],

    },
    created: function () {
        const vm = this;
        chats = axios.get('/chat/api/chats/')
            .then(function (response) {
                vm.chats = response.data
            });
    }
});