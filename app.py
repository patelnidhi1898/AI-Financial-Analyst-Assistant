import asyncio
import streamlit as st
import matplotlib.pyplot as plt
import import_ipynb 
import financial_analyst_nb_2                                                         

# Fix: Windows Python 3.13 asyncio ProactorEventLoop crash
if hasattr(asyncio, "WindowsSelectorEventLoopPolicy"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Direct import — no import_ipynb needed anymore
from financial_analyst_nb_2 import financial_analyst


def plot_stock(hist, company_name: str):
    fig, ax = plt.subplots(figsize=(10, 4))
    hist[["Open", "Close"]].plot(kind="line", ax=ax)
    ax.set_title(f"{company_name} — Stock Price (1Y)")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price (USD)")
    ax.legend(["Open", "Close"])
    ax.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    return fig


def main():
    st.set_page_config(
        page_title="AI Financial Analyst",
        page_icon="📈",
        layout="wide",
    )

    st.title("📈 AI Financial Analyst")
    st.caption(
        "Enter a company name or ticker to generate a full "
        "investment thesis with a BUY / HOLD / SELL recommendation."
    )

    company_name = st.text_input(
        "Company name or ticker",
        placeholder="e.g. Tesla, NVDA, Apple...",
    )

    analyze_button = st.button("Analyse", type="primary")

    if analyze_button:
        if not company_name.strip():
            st.warning("Please enter a company name before clicking Analyse.")
            return

        with st.spinner(f"Fetching data and generating thesis for **{company_name}**..."):
            try:
                result = financial_analyst(company_name)
            except Exception as e:
                st.error(f"Unexpected error during analysis: {e}")
                return

        if result is None:
            st.error(
                "Analysis failed — could not extract company/ticker or fetch data. "
                "Check the terminal for details."
            )
            return

        try:
            investment_thesis, hist = result
        except (TypeError, ValueError):
            st.error("Unexpected return format from financial_analyst().")
            return

        if not investment_thesis or not investment_thesis.strip():
            st.error("The model returned an empty thesis. Try again.")
            return

        st.subheader("Stock Price — Last 12 Months")
        if hist is None or hist.empty:
            st.warning("No stock price history available for this ticker.")
        else:
            try:
                fig = plot_stock(hist, company_name)
                st.pyplot(fig)
                plt.close(fig)
            except Exception as e:
                st.warning(f"Could not render price chart: {e}")

        st.subheader("Investment Thesis")
        st.markdown(investment_thesis, unsafe_allow_html=False)


if __name__ == "__main__":
    main()