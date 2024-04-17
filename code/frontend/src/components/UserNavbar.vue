<template>
  <div>
    <b-navbar toggleable="lg" type="light" variant="dark">
      <b-navbar-brand href="#">OSTS</b-navbar-brand>
      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav>
          <div class="buttons" v-for="b in nav_buttons" :key="b.id">
            <b-button
              variant="primary"
              :to="{ path: b.link }"
              @click="change_button_state(b.id)"
              :class="{ active: b.active }"
            >{{ b.title }}</b-button>
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
            </b-img>
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
    if (this.user_role === "staff") {
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

<style scoped>
/* Navbar styling */
nav {
  background-color: #222; /* Dark background color */
}

/* Navbar brand styling */
.navbar-brand {
  font-size: 24px;
  color: #ffffff; /* White color for text */
}

.b-navbar-brand {
  font-size: 24px;
  color: #ffffff; /* White color for text */
}

/* Navbar toggle button styling */
.b-navbar-toggle {
  border-color: #fff; /* White border color */
}

/* Navbar links styling */
.navbar-nav .nav-link {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; /* Update font */
  font-size: 18px; /* Increase font size */
  color: #fff; /* White color for text */
}

/* Active link styling */
.navbar-nav .nav-link.active {
  background-color: #4dd325; /* Green background color for active link */
  color: #fff; /* White color for text */
}

/* Profile picture button styling */
#profile_pic {
  width: 50px;
  height: 50px;
  border: 2px solid #fff; /* White border */
  border-radius: 50%; /* Circular shape */
  background-color: #ffffff;; /* Green background color */
}

/* Profile picture hover effect */
#profile_pic:hover {
  border-color: #bb0520; /* Green border color on hover */
}

/* Button styling */
.buttons {
  display: flex;
  flex-direction: column;
  align-items: center;
}
</style>

