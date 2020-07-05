<template>
  <div class="forum-widget-container" style="width: 100%; background-color: #ffffff">
    <v-container>
      <v-layout row>
        <v-flex xs1>{{content.no}}</v-flex>
        <v-flex xs3>[{{content.category}}]</v-flex>
        <v-flex xs4>{{content.title}}</v-flex>
        <v-flex xs3>by {{content.user}}</v-flex>
      </v-layout>
      <v-layout row>
        <v-flex xs8>{{content.uploaded_at}}</v-flex>
        <v-flex xs2>likes {{content.like}}</v-flex>
        <v-flex xs2>views {{content.view}}</v-flex>
      </v-layout>
    </v-container>
  </div>
  <v-btn>write</v-btn>
</template> 

<script>
import Vue from "vue";
import { mapMutations, mapGetters } from "vuex";

export default {
  // name: "InProgressLayout",
  name: "Item",
  components: {},
  props: {
    content: Object, //inprogress content object를 속성값으로 부모 component에서 전달받음
    index: Number //list에서의 index 값 부모 component에서 전달 받음 (항목 select 시 사용하기 위함)
  },
  data() {
    return {
      selected: false
    };
  },
  computed: {
    ...mapGetters(["isCheckBoxActivate"]),
    checkRefs() {
      Vue.$log.debug(`checkRefs -> ${JSON.stringify(this.$refs)}`);
    }
  },
  methods: {
    // # region Complete list 관련 함수
    ...mapMutations(["selectCompletedContent", "setCoin"])
    //content download 메서드
  }
};
</script>

<style lang="scss" scoped>
.card-wrapper {
  display: flex;
  position: relative;
  .thumbnail-container {
    position: relative;
    color: black;
    .thumbnail-img {
      width: 72px;
      height: 72px;
      background-size: 100% 100%;
      @media screen and (min-width: 1281px) {
        width: 100px;
        height: 56px;
      }
    }
  }
  .file-info-container {
    display: inline-block;
    width: 100%;
    padding: 2px 8px 2px 8px;
    @media screen and (min-width: 1281px) {
      height: 56px;
    }
    .content-title {
      display: inline-block;
      height: 18px;
      font-size: 15px;
      font-weight: 600;
      max-width: 600px;
      @media screen and (max-width: 1680px) {
        max-width: 450px;
      }
      @media screen and (max-width: 1280px) {
        max-width: 380px;
        font-size: 14px;
      }
      @media screen and (max-width: 768px) {
        max-width: 300px;
      }
      @media screen and (max-width: 480px) {
        max-width: 170px;
      }
    }

    .content-title-ext {
      display: inline-block;
      position: absolute;
      height: 18px;
      font-size: 14px;
      font-weight: 600;
      @media screen and (min-width: 1281px) {
        font-size: 15px;
      }
    }
    .thumbnail-tag {
      position: absolute;
      display: inline-block;
      width: 21px;
      height: 20px;
      top: 1px;
      left: 53px;
      color: white;
      white-space: nowrap;
      border-radius: 2px;
      font-size: 14px;
      font-weight: 800;
      padding: 0px 2px 0px 2px;
      background-color: grey;
      border: 1px solid white;
      @media screen and (max-width: 1280px) {
        width: 18px;
        height: 17px;
        font-size: 10px;
        font-weight: 800;
      }
    }

    .content-upload-date {
      max-width: 300px;
      overflow: hidden;
      white-space: nowrap;
      text-overflow: ellipsis;
      font-size: 0.7em;
    }

    @media screen and (min-width: 1281px) {
      padding: 18px 16px 18px 16px;
      .content-title {
        display: inline-block;
        vertical-align: top;
      }
      .content-title-ext {
        top: 18px;
      }
      .thumbnail-tag {
        top: 20px;
        left: 60%;
        position: absolute;
        font-size: 11px;
        padding: unset;
        text-align: center;
        color: gray;
        font-weight: 900;
        border: 2px solid gray;
        background-color: white;
      }
      .content-upload-date {
        display: inline-block;
        font-size: 15px;
        font-weight: 700;
        top: 19px;
        right: 17%;
        position: absolute;
        vertical-align: middle;
        color: #4c4c4c;
      }
    }
  }
  .content-status {
    position: relative;
    @media screen and (max-width: 768px) {
      position: absolute;
      left: 80px;
      bottom: 2px;
    }
    .loading-wrapper {
      display: inline-block;
      white-space: nowrap;
      position: relative;
      right: 56px;
      top: 4px;
      @media screen and (max-width: 1280px) {
        top: 13px;
      }
      @media screen and (max-width: 768px) {
        right: unset;
        top: unset;
      }
      .loading {
        width: 20px;
        height: 20px;
        top: 13px;
        right: 30px;
        object-fit: contain;
        animation: rotation 2s infinite linear;
        @media screen and (max-width: 1280px) {
          top: 9px;
        }
        @media screen and (max-width: 768px) {
          top: 13px;
          right: unset;
        }
      }
      @keyframes rotation {
        from {
          transform: rotate(0deg);
        }
        to {
          transform: rotate(359deg);
        }
      }
      .content-status-text {
        height: 16px;
        font-family: Roboto;
        font-size: 14px;
        font-weight: 500;
        font-stretch: normal;
        font-style: normal;
        line-height: 1.43;
        letter-spacing: -0.28px;
        text-align: right;
        color: #bfbfbf;

        .just-completed {
          font-family: Roboto;
          font-size: 14px;
          font-weight: 500;
          font-style: normal;
          font-stretch: normal;
          line-height: 1.67;
          letter-spacing: -0.24px;
          text-align: left;
          color: #2fd9d3;
          position: relative;
          top: 10px;
          @media screen and (max-width: 1280px) {
            top: 7px;
          }
          @media screen and (max-width: 768px) {
            top: unset;
          }
        }
        .status-text {
          position: absolute;
          top: 14px;
        }
        .percent {
          left: -7px;
        }
        .pending {
          right: 1px;
          font-size: 14px;
        }
        @media screen and (max-width: 1280px) {
          .status-text {
            top: 10px;
          }
        }
        @media screen and (max-width: 768px) {
          .pending {
            top: unset;
            right: unset;
          }
          .percent {
            top: 14px;
            left: 25px;
          }
        }
      }
    }
  }

  #item-menu-wrapper {
    position: absolute;
    top: 14px;
    right: 6px;
    @media screen and (max-width: 1280px) {
      top: 18px;
      right: 16px;
      display: inline-block;
    }
    #content-download-btn {
      position: relative;
    }
    #item-menu {
      align-self: baseline;
      // margin: 8px 0px 0px 0px;
    }
  }
}
</style>
