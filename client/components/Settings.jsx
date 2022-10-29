import React from 'react';
import { hot } from 'react-hot-loader';

/**
 * Settings component
 */
class Settings extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      loading: true,
      error: false,
      watchlist: undefined,
    };
    /**
     * Common headers
     */
    this.headers = {
      Accept: 'application/json',
      'Content-Type': 'application/json',
      'X-CSRFToken': this.getCookie('csrftoken'),
    };
    /**
     * Api endpoint base url
     */
    this.url = '/api/v1/watchlist/';
  }

  componentWillMount() {
    this.getWatchlist();
  }

  /**
   * Helper to get required cookies
   */
  getCookie = name => {
    if (!document.cookie) {
      return null;
    }

    const xsrfCookies = document.cookie
      .split(';')
      .map(c => c.trim())
      .filter(c => c.startsWith(name + '='));

    if (xsrfCookies.length === 0) {
      return null;
    }

    return decodeURIComponent(xsrfCookies[0].split('=')[1]);
  };

  /**
   * Gets watchlist for user
   */
  getWatchlist() {
    fetch(this.url, {
      method: 'GET',
      headers: this.headers,
      credentials: 'same-origin',
    })
      .then(res => {
        if (res.status !== 200) {
          return this.setState({
            loading: false,
            error: true,
          });
        }
        return res.json();
      })
      .then(data => {
        this.setState({
          watchlist: data.results,
          loading: false,
          error: false,
        });
      })
      .catch();
  }

  /**
   * Handles unwatching
   */
  unwatch = ticker => {
    fetch(this.url + ticker + '/', {
      method: 'DELETE',
      headers: this.headers,
      credentials: 'same-origin',
    })
      .then(() => {
        this.getWatchlist();
      })
      .catch();
  };

  render() {
    const { watchlist, error, loading } = this.state;

    if (loading) return 'Loading...';
    if (error) return 'An error has occurred.';

    return (
      <div className="watchlist">
        <h3>Watchlist</h3>
        <table className="table table-document">
          <thead>
            <tr>
              <th className="col-md-2">Ticker</th>
              <th className="col-md-8">Company</th>
              <th className="col-md-2" />
            </tr>
          </thead>
          <tbody>
            {watchlist.map(item => {
              let url = '/company/' + item.company.ticker;
              if (item.company.ticker === undefined) {
                url = '/company/' + item.company.id;
              }
              return (
                <tr key={item.company.id}>
                  <td>{item.company.ticker}</td>
                  <td>
                    <a href={url}>{item.company.short_name}</a>
                  </td>
                  <td>
                    <button
                      className="btn-link"
                      type="button"
                      onClick={() => this.unwatch(item.company.ticker)}>
                      Unwatch
                    </button>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    );
  }
}

export default hot(module)(Settings);
