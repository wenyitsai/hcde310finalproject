import requests
import streamlit as st
from api_key import key1

API_KEY = key1
BASE_URL = 'https://serpapi.com/search.json'


def fetch_fashion_items(query):
    try:
        params = {
            'engine': 'google_shopping',
            'q': query,
            'api_key': API_KEY
        }
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get('shopping_results', [])
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data for '{query}': {e}")
        return []


def extract_price_value(price_string):
    """Extract numeric price value from price string"""
    if not price_string or price_string == "Price not available":
        return None

    import re
    numbers = re.findall(r'[\d,]+\.?\d*', str(price_string).replace(',', ''))
    if numbers:
        try:
            return float(numbers[0])
        except ValueError:
            return None
    return None


def filter_results_by_price(results, min_price=None, max_price=None):
    """Filter results based on price range"""
    if not min_price and not max_price:
        return results

    filtered_results = []
    for item in results:
        price_str = item.get("price", "")
        price_value = extract_price_value(price_str)

        if price_value is None:
            continue

        include_item = True
        if min_price and price_value < min_price:
            include_item = False
        if max_price and price_value > max_price:
            include_item = False

        if include_item:
            filtered_results.append(item)

    return filtered_results


def display_results(results, show_price_stats=True):
    if not results:
        return

    if show_price_stats and len(results) > 1:
        prices = []
        for item in results:
            price_val = extract_price_value(item.get("price", ""))
            if price_val:
                prices.append(price_val)

        if prices:
            min_price = min(prices)
            max_price = max(prices)
            avg_price = sum(prices) / len(prices)

            st.markdown(f"""
            <div style='
                background: linear-gradient(135deg, #e8f5e8, #fff3e0);
                padding: 15px;
                border-radius: 12px;
                margin-bottom: 20px;
                border: 2px solid #4caf50;
                text-align: center;
            '>
                <h4 style='color: #2e7d32; margin: 0 0 10px 0;'>💰 Price Range Summary</h4>
                <div style='display: flex; justify-content: space-around; flex-wrap: wrap;'>
                    <span style='color: #388e3c; font-weight: bold;'>Min: ${min_price:.2f}</span>
                    <span style='color: #f57c00; font-weight: bold;'>Avg: ${avg_price:.2f}</span>
                    <span style='color: #d32f2f; font-weight: bold;'>Max: ${max_price:.2f}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    cols_per_row = 2
    for i in range(0, len(results[:6]), cols_per_row):
        cols = st.columns(cols_per_row)
        for j, col in enumerate(cols):
            if i + j < len(results):
                item = results[i + j]
                with col:
                    with st.container():
                        st.markdown("""
                        <div style='
                            background: linear-gradient(135deg, #fff9c4 0%, #fce4ec 50%, #e8f5e8 100%);
                            padding: 20px;
                            border-radius: 15px;
                            box-shadow: 0 10px 30px rgba(255,182,193,0.3);
                            margin-bottom: 20px;
                            border: 2px solid #ffeb3b;
                        '>
                        """, unsafe_allow_html=True)

                        img = item.get("thumbnail")
                        if img:
                            st.markdown(f"""
                            <div style='text-align: center; margin-bottom: 15px;'>
                                <img src='{img}' style='
                                    width: 100%;
                                    max-width: 200px;
                                    height: 200px;
                                    object-fit: cover;
                                    border-radius: 10px;
                                    box-shadow: 0 5px 15px rgba(0,0,0,0.3);
                                ' />
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown("""
                            <div style='
                                text-align: center;
                                padding: 60px 20px;
                                background: linear-gradient(135deg, #ffcccb, #ffe4e1);
                                border-radius: 10px;
                                margin-bottom: 15px;
                                color: #d32f2f;
                                border: 2px dashed #ff69b4;
                            '>
                                📷 No image available
                            </div>
                            """, unsafe_allow_html=True)

                        title = item.get("title", "No title")
                        st.markdown(f"""
                        <h4 style='
                            color: #2e7d32;
                            margin: 0 0 10px 0;
                            font-size: 16px;
                            line-height: 1.4;
                            text-align: center;
                            font-weight: 600;
                            text-shadow: 1px 1px 2px rgba(255,255,255,0.8);
                        '>{title}</h4>
                        """, unsafe_allow_html=True)

                        price = item.get("price", "Price not available")
                        st.markdown(f"""
                        <div style='
                            text-align: center;
                            margin-bottom: 15px;
                        '>
                            <span style='
                                background: linear-gradient(135deg, #ffeb3b, #ff9800);
                                color: #d84315;
                                padding: 8px 16px;
                                border-radius: 20px;
                                font-size: 18px;
                                font-weight: bold;
                                box-shadow: 0 3px 10px rgba(255,152,0,0.4);
                                border: 2px solid #ff6f00;
                            '>💰 {price}</span>
                        </div>
                        """, unsafe_allow_html=True)

                        link = item.get("link") or item.get("product_link") or item.get("serpapi_product_api")

                        source = item.get("source", "")

                        if link and link != "#":
                            st.markdown(f"""
                            <div style='text-align: center;'>
                                <a href='{link}' target='_blank' rel='noopener noreferrer' style='text-decoration: none;'>
                                    <button style='
                                        background: linear-gradient(135deg, #ff6b9d, #ffa726);
                                        color: white;
                                        border: none;
                                        padding: 12px 24px;
                                        border-radius: 25px;
                                        cursor: pointer;
                                        font-size: 16px;
                                        font-weight: bold;
                                        transition: all 0.3s ease;
                                        box-shadow: 0 4px 15px rgba(255, 107, 157, 0.4);
                                        width: 100%;
                                    ' onmouseover='this.style.transform="translateY(-2px)"; this.style.boxShadow="0 6px 20px rgba(255, 107, 157, 0.6)"' 
                                      onmouseout='this.style.transform="translateY(0px)"; this.style.boxShadow="0 4px 15px rgba(255, 107, 157, 0.4)"'>
                                        🛒 Buy at {source}
                                    </button>
                                </a>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown("""
                            <div style='text-align: center;'>
                                <div style='
                                    background: linear-gradient(135deg, #e0e0e0, #bdbdbd);
                                    color: #666;
                                    border: none;
                                    padding: 12px 24px;
                                    border-radius: 25px;
                                    font-size: 16px;
                                    width: 100%;
                                    text-align: center;
                                '>
                                    🔍 Search manually
                                </div>
                            </div>
                            """, unsafe_allow_html=True)

                        st.markdown("</div>", unsafe_allow_html=True)


def main():
    st.set_page_config(
        page_title="SnipeStyle - Fashion Search",
        page_icon="🎯",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    st.markdown("""
    <style>
    .main > div {
        padding-top: 2rem;
    }

    .stApp {
        background: linear-gradient(135deg, #fff9c4 0%, #fce4ec 25%, #e8f5e8 50%, #fff3e0 75%, #f3e5f5 100%);
        min-height: 100vh;
    }

    .search-header {
        text-align: center;
        padding: 40px 20px;
        background: linear-gradient(135deg, #fff9c4, #fce4ec);
        border-radius: 20px;
        margin-bottom: 30px;
        border: 3px solid #ffeb3b;
        box-shadow: 0 8px 25px rgba(255,235,59,0.3);
    }

    .search-form {
        background: linear-gradient(135deg, #e8f5e8, #fff3e0);
        padding: 30px;
        border-radius: 15px;
        border: 2px solid #4caf50;
        margin-bottom: 30px;
        box-shadow: 0 5px 20px rgba(76,175,80,0.2);
    }

    .stTextInput > div > div > input {
        background: linear-gradient(135deg, #fff9c4, #ffffff);
        border: 2px solid #ff69b4;
        border-radius: 10px;
        color: #2e7d32;
        padding: 12px;
        font-weight: 500;
    }

    .stTextInput > div > div > input::placeholder {
        color: #81c784;
        font-style: italic;
    }

    .stButton > button {
        background: linear-gradient(135deg, #ff6b9d, #ffa726, #66bb6a);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 15px 30px;
        font-size: 18px;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 5px 20px rgba(255,107,157,0.4);
        width: 100%;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(255,107,157,0.6);
    }

    .results-header {
        background: linear-gradient(135deg, #fce4ec, #fff3e0);
        padding: 20px;
        border-radius: 15px;
        margin: 20px 0;
        border: 2px solid #ff69b4;
        box-shadow: 0 5px 15px rgba(255,105,180,0.3);
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='search-header'>
        <h1 style='
            font-size: 48px;
            margin: 0;
            background: linear-gradient(135deg, #ff6b9d, #ffa726, #66bb6a);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        '>🎯 SnipeStyle</h1>
        <p style='
            font-size: 20px;
            color: #2e7d32;
            margin: 10px 0 0 0;
            font-weight: 600;
            text-shadow: 1px 1px 2px rgba(255,255,255,0.8);
        '>Discover and snipe the hottest fashion trends instantly</p>
        <div style='
            width: 60px;
            height: 4px;
            background: linear-gradient(135deg, #ff6b9d, #ffa726);
            margin: 20px auto;
            border-radius: 2px;
        '></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='search-form'>", unsafe_allow_html=True)
    st.markdown(
        "<h3 style='color: #2e7d32; text-align: center; margin-bottom: 20px; text-shadow: 1px 1px 2px rgba(255,255,255,0.8);'>🔍 Search for Fashion Items</h3>",
        unsafe_allow_html=True)

    with st.form("search_form", clear_on_submit=False):
        st.markdown("<h4 style='color: #d32f2f; margin-bottom: 15px;'>🛍️ What are you looking for?</h4>",
                    unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)

        queries = []
        with col1:
            q1 = st.text_input("Search term 1", placeholder="e.g., designer sneakers", key="query_1")
            if q1: queries.append(q1.strip())

        with col2:
            q2 = st.text_input("Search term 2", placeholder="e.g., vintage jacket", key="query_2")
            if q2: queries.append(q2.strip())

        with col3:
            q3 = st.text_input("Search term 3", placeholder="e.g., luxury handbag", key="query_3")
            if q3: queries.append(q3.strip())

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<h4 style='color: #d32f2f; margin-bottom: 15px;'>💰 Price Range (Optional)</h4>",
                    unsafe_allow_html=True)

        price_col1, price_col2, price_col3 = st.columns([1, 1, 1])

        with price_col1:
            min_price = st.number_input(
                "Minimum Price ($)",
                min_value=0.0,
                max_value=10000.0,
                value=0.0,
                step=5.0,
                key="min_price"
            )

        with price_col2:
            max_price = st.number_input(
                "Maximum Price ($)",
                min_value=0.0,
                max_value=10000.0,
                value=1000.0,
                step=5.0,
                key="max_price"
            )

        with price_col3:
            st.markdown("<label style='color: #2e7d32; font-weight: bold;'>Quick Filters:</label>",
                        unsafe_allow_html=True)
            budget_filter = st.selectbox(
                "Budget Range",
                ["Custom", "Under $25", "$25-$50", "$50-$100", "$100-$250", "$250-$500", "$500+"],
                key="budget_filter"
            )

        if budget_filter != "Custom":
            if budget_filter == "Under $25":
                min_price, max_price = 0, 25
            elif budget_filter == "$25-$50":
                min_price, max_price = 25, 50
            elif budget_filter == "$50-$100":
                min_price, max_price = 50, 100
            elif budget_filter == "$100-$250":
                min_price, max_price = 100, 250
            elif budget_filter == "$250-$500":
                min_price, max_price = 250, 500
            elif budget_filter == "$500+":
                min_price, max_price = 500, 10000

        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("🚀 Start Sniping")

    st.markdown("</div>", unsafe_allow_html=True)

    if submitted and queries:
        if min_price > 0 or max_price < 1000:
            st.markdown(f"""
            <div style='
                background: linear-gradient(135deg, #fff3e0, #fce4ec);
                padding: 15px;
                border-radius: 12px;
                margin: 20px 0;
                border: 2px solid #ff9800;
                text-align: center;
            '>
                <h4 style='color: #f57c00; margin: 0;'>🎯 Active Price Filter: ${min_price:.0f} - ${max_price:.0f}</h4>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div style='text-align: center; margin: 30px 0;'>
            <h2 style='color: #2e7d32; font-size: 28px; text-shadow: 1px 1px 2px rgba(255,255,255,0.8);'>🎉 Your Fashion Finds</h2>
        </div>
        """, unsafe_allow_html=True)

        for i, query in enumerate(queries):
            st.markdown(f"""
            <div class='results-header'>
                <h3 style='
                    color: #d32f2f;
                    margin: 0;
                    font-size: 24px;
                    text-shadow: 1px 1px 2px rgba(255,255,255,0.8);
                '>👗 Results for: "<span style='color: #ff6b9d;'>{query}</span>"</h3>
            </div>
            """, unsafe_allow_html=True)

            with st.spinner(f"Sniping the best {query} deals..."):
                results = fetch_fashion_items(query)

            if results:
                filtered_results = filter_results_by_price(results, min_price if min_price > 0 else None,
                                                           max_price if max_price < 1000 else None)

                if filtered_results:
                    if len(filtered_results) != len(results):
                        st.markdown(f"""
                        <div style='
                            background: linear-gradient(135deg, #e8f5e8, #f3e5f5);
                            padding: 10px;
                            border-radius: 8px;
                            margin-bottom: 15px;
                            text-align: center;
                            border: 1px solid #4caf50;
                        '>
                            <span style='color: #2e7d32; font-weight: bold;'>
                                📊 Showing {len(filtered_results)} of {len(results)} items in your price range
                            </span>
                        </div>
                        """, unsafe_allow_html=True)

                    display_results(filtered_results)
                else:
                    st.markdown(f"""
                    <div style='
                        text-align: center;
                        padding: 40px;
                        background: linear-gradient(135deg, #ffcccb, #ffe4e1);
                        border-radius: 15px;
                        margin: 20px 0;
                        border: 2px dashed #ff69b4;
                    '>
                        <h4 style='color: #d32f2f; text-shadow: 1px 1px 2px rgba(255,255,255,0.8);'>💸 No items found in price range ${min_price:.0f} - ${max_price:.0f}</h4>
                        <p style='color: #f57c00; font-weight: 500;'>Try adjusting your price filter or search terms</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style='
                    text-align: center;
                    padding: 40px;
                    background: linear-gradient(135deg, #ffcccb, #ffe4e1);
                    border-radius: 15px;
                    margin: 20px 0;
                    border: 2px dashed #ff69b4;
                '>
                    <h4 style='color: #d32f2f; text-shadow: 1px 1px 2px rgba(255,255,255,0.8);'>😔 No results found for this search</h4>
                    <p style='color: #f57c00; font-weight: 500;'>Try different keywords or check your spelling</p>
                </div>
                """, unsafe_allow_html=True)

    elif submitted and not queries:
        st.warning("Please enter at least one search term!")

    st.markdown("""
    <div style='
        text-align: center;
        margin-top: 50px;
        padding: 20px;
        color: #2e7d32;
        border-top: 3px solid #ff69b4;
        background: linear-gradient(135deg, #fff9c4, #fce4ec);
        border-radius: 15px;
    '>
        <p style='font-weight: 600; text-shadow: 1px 1px 2px rgba(255,255,255,0.8);'>Made with ❤️ for fashion enthusiasts | Powered by SerpAPI</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()