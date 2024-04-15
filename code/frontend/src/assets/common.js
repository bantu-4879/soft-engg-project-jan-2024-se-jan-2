/* eslint-disable */

const BASEURL = "http://127.0.0.1:5000";
const VERSION = "v2";

const AUTH_API_PREFIX = `/api/${VERSION}/auth`;
const STUDENT_API_PREFIX = `/api/${VERSION}/student`;
const SUPPORT_API_PREFIX = `/api/${VERSION}/staff`;
const ADMIN_API_PREFIX = `/api/${VERSION}/admin`;
const FAQ_API_PREFIX = `/api/${VERSION}/faq/`;
const TICKET_API_PREFIX = `/api/${VERSION}/ticket`
const DISCOURSE_AUTH_PREFIX = `//api/${VERSION}/discourseAuth`
const DISCOURSE_POST_PREFIX = `/api/${VERSION}/discourse`
const INBOX_API_PREFIX = `/api/${VERSION}/inbox`
const USER_MANAGEMENT_PREFIX = `/api/${VERSION}/management`
const USERDETAILS_PREFIX = `/api/${VERSION}/userDetails`
const STATS_PREFIX = `/api/${VERSION}/data`

const AUTH_API_LOGIN = `${BASEURL}${AUTH_API_PREFIX}/login`
const AUTH_API_REGISTER = `${BASEURL}${AUTH_API_PREFIX}/register`
const AUTH_API_NEWUSERS = `${BASEURL}${AUTH_API_PREFIX}/newUsers`

const STUDENT_API = `${BASEURL}${STUDENT_API_PREFIX}`;
const SUPPORT_API = `${BASEURL}${SUPPORT_API_PREFIX}`;
const ADMIN_API = `${BASEURL}${ADMIN_API_PREFIX}`;
const FAQ_API = `${BASEURL}${FAQ_API_PREFIX}`;
const TICKET_API = `${BASEURL}${TICKET_API_PREFIX}`;
const DISCOURSE_REGISTER_API = `${BASEURL}${DISCOURSE_AUTH_PREFIX}`
const INBOX_API = `${BASEURL}${INBOX_API_PREFIX}`
const MANAGEMENT_API = `${BASEURL}${USER_MANAGEMENT_PREFIX}`
const USERDETAILS_API = `${BASEURL}${USERDETAILS_PREFIX}`
const STATS_API = `${BASEURL}${STATS_PREFIX}`
const DISCOURSE_TICKET_API=`${BASEURL}${DISCOURSE_POST_PREFIX}`
const TICKET_API_ALLTICKETS = `${BASEURL}${TICKET_API_PREFIX}/all-tickets`
const WEBHOOK_URL_STAFF = `https://chat.googleapis.com/v1/spaces/AAAAsTbnkos/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=2ZVePrYB_1cEwSrlkdUstzpUGCFBW9a6_RtzylmGdQE`
const WEBHOOK_URL_STUDENT = `https://chat.googleapis.com/v1/spaces/AAAAsTbnkos/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=aJjfYWhYMscOv6l-VukfKhX3c3GhRmN3Xpg_KAt03p4`
const WEBHOOK_URL_ADMIN = `https://chat.googleapis.com/v1/spaces/AAAAsTbnkos/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=VgCumRm7zG5aykpSjHoQ9bZ9FG3i2LSZEdmMlcD_CBA`


const STUDENT_ROUTES = ['/student', '/student-home', "/student-create-ticket", "/student-my-tickets", "/common-faqs", "/user-profile", "/inbox"]
const SUPPORT_ROUTES = ['/staff', '/staff-home', "/staff-my-tickets", "/common-faqs", "/user-profile", "/inbox"]
const ADMIN_ROUTES = ['/admin', '/admin-home', "/admin-create-faq", "/admin-validate-users", "/common-faqs", "/user-profile","/inbox", "/user-management"]


const STUDENT_NAV_BUTTONS = [
  { id: 1, title: "Home", link: "/student-home", active: false },
  { id: 2, title: "Create Ticket", link: "/student-create-ticket", active: false },
  { id: 3, title: "My Tickets", link: "/student-my-tickets", active: false },
  { id: 4, title: "FAQs", link: "/common-faqs", active: false },
  { id: 5, title: "Inbox", link: "/inbox", active: false },
  { id: 6, title: "Logout", link: "#", active: false },
]

const SUPPORT_NAV_BUTTONS = [
  { id: 1, title: "Home", link: "/staff-home", active: false },
  { id: 2, title: "My Tickets", link: "/staff-my-tickets", active: false },
  { id: 3, title: "FAQs", link: "/common-faqs", active: false },
  { id: 4, title: "Logout", link: "#", active: false },
]

const ADMIN_NAV_BUTTONS = [
  { id: 1, title: "Home", link: "/admin-home", active: false },
  { id: 2, title: "Validate Users", link: "/admin-validate-users", active: false },
  { id: 3, title: "Create FAQ", link: "/admin-create-faq", active: false },
  { id: 4, title: "FAQs", link: "/common-faqs", active: false },
  { id: 5, title: "Inbox", link: "/inbox", active: false },
  { id: 6, title: "User Management", link: "/user-management", active: false },
  { id: 7, title: "Logout", link: "#", active: false },
]

export {
  AUTH_API_LOGIN,
  AUTH_API_REGISTER,
  AUTH_API_NEWUSERS,
  STUDENT_API_PREFIX,
  SUPPORT_API_PREFIX,
  ADMIN_API_PREFIX,
  FAQ_API_PREFIX,
  TICKET_API_ALLTICKETS,
  TICKET_API_PREFIX,
  STUDENT_API,
  SUPPORT_API,
  ADMIN_API,
  FAQ_API,
  TICKET_API,
  STUDENT_ROUTES,
  SUPPORT_ROUTES,
  ADMIN_ROUTES,
  STUDENT_NAV_BUTTONS,
  SUPPORT_NAV_BUTTONS,
  ADMIN_NAV_BUTTONS, 
  WEBHOOK_URL_ADMIN,
  WEBHOOK_URL_STUDENT,
  WEBHOOK_URL_STAFF,
  DISCOURSE_REGISTER_API,
  INBOX_API, 
  MANAGEMENT_API,
  USERDETAILS_API,
  DISCOURSE_TICKET_API,
  STATS_API
};
