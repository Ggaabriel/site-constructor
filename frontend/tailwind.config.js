/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    fontFamily: {
      sans: ["montserrat", "sans-serif"],
    },
    extend: {
      colors: {
        start: "#7942D1",
        end: "#E74EEA",
        accent: "#FF78E9",
        main: "#FFFFFF",
        project: "#B96CE3",
        addProject: "#9F46D9",
        mainBlack: "#292929",
      },
      borderWidth: {
        3: "3px",
      },
      borderRadius: {
        20: "20px",
      },
      fontSize: {
        24: "24px",
        20: "20px",
        16: "16px",
        14: "14px",
        12: "12px",
      },
    },
  },
  plugins: [],
};
