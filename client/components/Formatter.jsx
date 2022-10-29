import moment from 'moment';

const F = {
  date(date) {
    return moment(date).format('DD/MM/YY');
  },

  capitalize(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
  },
};

export default F;
