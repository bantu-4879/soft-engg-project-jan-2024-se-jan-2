<template>
  <div>
    <b-navbar toggleable="lg" type="light" variant="light">
      <b-navbar-brand href="#">OSTS</b-navbar-brand>
      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav>
          <div class="buttons" v-for="b in nav_buttons" :key="b.id">
            <b-button
              variant="primary"
              :to="{ path: b.link }"
              @click="change_button_state(b.id)"
              :style="{
                boxShadow: b.active ? '5px 5px 15px 5px #a3a3a3' : 'none',
                backgroundColor: b.active ? 'blue' : '#f8f9fa',
                color: b.active ? 'white' : 'black',
                borderColor: b.active ? '#007bff' : '#f8f9fa',
                fontSize: b.active ? '18px' : '16px',
              }"
              >{{ b.title }}</b-button
            >
          </div>
        </b-navbar-nav>

        <!-- Right aligned nav items -->
        <b-navbar-nav class="ml-auto">
          <b-button
            id="profile_pic"
            :to="{ path: user_profile_page_url }"
            @click="change_button_state(0)"
            ><b-img
              :src="profile_pic_base64"
              v-bind="mainProps"
              alt="Profile image"
              style="margin: -6px -10px -12px -12px"
            ></b-img>
          </b-button>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
  </div>
</template>

<script>
import * as common from "../assets/common.js";

export default {
  name: "UserNavbar",
  props: ["id_"],
  components: {},
  data() {
    return {
      mainProps: { width: 50, height: 50 },
      user_id: this.$store.getters.get_user_id,
      user_role: this.$store.getters.get_user_role,
      user_url_to_fetch_data: "",
      user_profile_page_url: "",
      profile_pic_base64: this.$store.getters.get_user_profile_pic,
      nav_buttons: null,
    };
  },
  created() {
    if (this.user_role === "student") {
      this.user_profile_page_url = "/user-profile";
      this.nav_buttons = common.STUDENT_NAV_BUTTONS;
    }
    if (this.user_role === "support") {
      this.user_profile_page_url = "/user-profile";
      this.nav_buttons = common.SUPPORT_NAV_BUTTONS;
    }
    if (this.user_role === "admin") {
      this.user_profile_page_url = "/user-profile";
      this.nav_buttons = common.ADMIN_NAV_BUTTONS;
    }

    for (let b of this.nav_buttons) {
      if (b.id == this.id_) {
        b.active = true;
      } else {
        b.active = false;
      }
    }
  },
  mounted() {},
  methods: {
    change_button_state(id_) {
      let current_title = "";
      for (let b of this.nav_buttons) {
        if (b.id == id_) {
          b.active = true;
          current_title = b.title;
        } else {
          b.active = false;
        }
      }
      if (current_title === "Logout") {
        // logout pressed
        // On logout -> delete user data
        this.$store.dispatch("set_state_after_logout", {});
        this.$router.push("/login");
      }
    },
  },
  computed: {},
};
</script>

<style>
nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #4dd325;
}

nav a.router-link-exact-active {
  color: #441ada;
}

.buttons {
  margin: 15px;
  justify-content: space-between;
}

#profile_pic {
  width: 50px;
  height: 50px;
  border: none;
  color: white;
}

#profile_pic:hover {
  border: none;
  color: white;
}

router-link {
  box-shadow: 5px 10px 8px 10px #888888;
  background-color: aqua;
}
</style>
