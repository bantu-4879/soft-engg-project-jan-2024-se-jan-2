import Vue from 'vue';
import Vuex from 'vuex';
import router from '../router';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    user: {
      user_id: "",
      role: "",
      first_name: "",
      last_name: "",
      email: "",
      profile_photo_loc: "",
    },
    web_token: "",
    token_expiry_on: 0,
    logged_status: false,
    timeout_id: null,
  },
  getters: {
    get_user: function (state) {
      return state.user
    },
    get_user_id: function (state) {
      return state.user.user_id
    },
    get_user_role: function (state) {
      return state.user.role
    },
    get_user_profile_pic: function (state) {
      return state.user.profile_photo_loc
    },
    get_web_token: function (state) {
      return state.web_token
    },
    get_token_expiry_on: function (state) {
      return state.token_expiry_on
    },
    get_logged_status: function (state) {
      return state.logged_status
    },

  },
  mutations: {
    initialiseStore(state) {
      // Check if the ID exists
      if (localStorage.getItem('store')) {
        console.log('App creating. Store available in local storage');
        // Replace the state object with the stored item
        this.replaceState(
          Object.assign(state, JSON.parse(localStorage.getItem('store')))
        );
      }
    },

    SET_STATE_AFTER_LOGIN(state, payload) {
      state.user.first_name = payload.first_name;
      state.user.last_name = payload.last_name;
      state.user.email = payload.email;
      state.user.user_id = payload.user_id;
      state.user.role = payload.role;
      state.web_token = payload.web_token;
      state.token_expiry_on = payload.token_expiry_on;
      state.user.profile_photo_loc = payload.profile_photo_loc;
      state.logged_status = true;
    },
    SET_STATE_AFTER_LOGOUT(state, payload) {
      state.user.first_name = "";
      state.user.last_name = "";
      state.user.email = "";
      state.user.user_id = "";
      state.user.role = "";
      state.web_token = "";
      state.token_expiry_on = 0;
      state.user.profile_photo_loc = "";
      state.logged_status = false;
      clearTimeout(state.timeout_id);
    },
    SET_STATE_AFTER_PROFILE_UPDATE(state, payload) {
      state.user.first_name = payload.first_name;
      state.user.last_name = payload.last_name;
      state.user.email = payload.email;
      state.user.profile_photo_loc = payload.profile_photo_loc;
    },
    SET_TIMEOUT_ID(state, payload) {
      state.timeout_id = payload;
    }
  },
  actions: {
    set_state_after_login(context, payload) {
      context.commit('SET_STATE_AFTER_LOGIN', payload);
    },
    set_state_after_logout(context, payload) {
      context.commit('SET_STATE_AFTER_LOGOUT', payload);
    },
    set_state_after_profile_update(context, payload) {
      context.commit('SET_STATE_AFTER_PROFILE_UPDATE', payload);
    },
    token_timeout_fn: async function (context, payload) {
      // delete token after timeout
      const timeout_id = setTimeout(function () {
        alert("Token Expired. Please login again");
        context.commit('SET_STATE_AFTER_LOGOUT', payload);
        router.push("/login");
      }, 1 * 60 * 1000);  // 1000 means 1 sec
      context.commit('SET_TIMEOUT_ID', timeout_id);
    },
  },
  modules: {
  },
});
