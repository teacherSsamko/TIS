
<template>
    <v-container column class="content-list-header-text" align-center style="margin-bottom: 30px;">
        <v-layout class="content-list-header-text" row align-left style="width:100%">
            <v-flex align-self-start>
                <div class="Coin-purchase" style="width:100%">Forum</div>
            </v-flex>
        </v-layout>
        <v-layout column style="width:100%">
            <v-flex>
                <div class="content-list">
                    <div class="content-list-detail" v-for="forum in forums" :key="forum.no">
                        <board-list :content="forum"></board-list>
                    </div>
                </div>
            </v-flex>
            <v-flex>
                <!-- detail here -->
            </v-flex>
            <v-flex>
                <!-- write page here -->
            </v-flex>
            
        </v-layout>
        <v-layout row align-right style="width:100%">
            <v-flex xs12 class="text-align-right">
                <button class="btn btn-primary" @click="writePost">write</button>
            </v-flex>
        </v-layout>
        
    </v-container>
</template>

<script>
    import Vue from 'vue';
    import { mapGetters, mapMutations } from "vuex";
    import BoardList from "Components/widget/forum/BoardList";
    

    const common = require('../../lib/common');

    
    export default {
        name: "Store",
        components: {
            BoardList
        },
        data() {
            return {
                storeList: [],
                forums: [
                    {
                        no: 1,
                        user: "ssamko",
                        category: "help",
                        title: "hi",
                        content: "gdf",
                        view: 1,
                        like: 1,
                        uploaded_at: "2020-07-01 18:07"
                    },{
                        no: 2,
                        user: "Jamie",
                        category: "idea",
                        title: "hello",
                        content: "ring ding dong",
                        view: 1,
                        like: 1,
                        uploaded_at: "2020-07-03 08:17"
                    }
                ],
                replies: [
                    {
                        forumNo: 1,
                        user: "Jamie",
                        text: "wow"
                    },{
                        forumNo: 2,
                        user: "JK",
                        text: "What?"
                    }

                ]
            }
        },
        computed: {
            ...mapGetters(["getUser"])
        },
        beforeCreate() {
            // 로그인이 안되어 있는 경우 로그인 페이지로 이동
            if (!this.$store.state.user.loginState) {
                this.$router.push("/user/login");
            } else {
                // 로그인이 되어 있는 경우, 스토어 아이템 리스트를 불러온다
                
            }
        },
        mounted() {
            
        },
        methods: {
            ...mapMutations([
                "setCoin"
            ]),
            writePost: function(){
                alert('write!')
            }
        }
    }
    
</script>

<style scoped>
.content-list-detail {
    margin-bottom: 8px;
    cursor: pointer;
}
/* .content-list-detail:hover {
    background-color: #999999;
} */
</style>
