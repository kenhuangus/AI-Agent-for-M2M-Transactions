import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import json

# Initialize session state
if 'transactions' not in st.session_state:
    st.session_state.transactions = []
if 'machines' not in st.session_state:
    st.session_state.machines = {
        'Machine-A': {'did': 'did:machine:a1b2c3', 'status': 'active', 'trust_score': 95},
        'Machine-B': {'did': 'did:machine:d4e5f6', 'status': 'active', 'trust_score': 88},
        'Machine-C': {'did': 'did:machine:g7h8i9', 'status': 'active', 'trust_score': 92},
    }

def generate_transaction():
    machines = list(st.session_state.machines.keys())
    sender = random.choice(machines)
    receiver = random.choice([m for m in machines if m != sender])
    
    transaction = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'sender': sender,
        'receiver': receiver,
        'amount': round(random.uniform(1, 1000), 2),
        'status': 'pending',
        'smart_contract': f'SC_{random.randint(1000, 9999)}',
        'ai_risk_score': round(random.uniform(0, 100), 2)
    }
    return transaction

def update_transaction_status(transaction):
    if transaction['ai_risk_score'] > 80:
        return 'rejected'
    elif transaction['ai_risk_score'] > 60:
        return 'flagged'
    else:
        return 'completed'

# Streamlit UI
st.title('M2M Transaction System')

# Sidebar for System Status
st.sidebar.header('System Status')
ai_status = st.sidebar.success('AI Agent: Active')
blockchain_status = st.sidebar.success('Blockchain Network: Connected')
smart_contract_status = st.sidebar.success('Smart Contracts: Operational')

# Main Dashboard Tabs
tab1, tab2, tab3, tab4 = st.tabs(['Dashboard', 'Machines', 'Transactions', 'Analytics'])

with tab1:
    st.header('System Overview')
    
    # Add new transaction button
    if st.button('Simulate New Transaction'):
        new_transaction = generate_transaction()
        new_transaction['status'] = update_transaction_status(new_transaction)
        st.session_state.transactions.append(new_transaction)
        st.success('New transaction generated!')
    
    # Display recent transactions
    if st.session_state.transactions:
        df = pd.DataFrame(st.session_state.transactions)
        
        # Create metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric('Total Transactions', len(df))
        with col2:
            st.metric('Success Rate', f"{(len(df[df['status'] == 'completed']) / len(df) * 100):.1f}%")
        with col3:
            st.metric('Average Risk Score', f"{df['ai_risk_score'].mean():.1f}")
        
        # Transaction status chart
        status_counts = df['status'].value_counts()
        fig_status = px.pie(values=status_counts.values, names=status_counts.index, 
                          title='Transaction Status Distribution')
        st.plotly_chart(fig_status)

with tab2:
    st.header('Registered Machines')
    
    for machine, details in st.session_state.machines.items():
        with st.expander(f"{machine} - DID: {details['did']}"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"Status: {details['status']}")
            with col2:
                st.write(f"Trust Score: {details['trust_score']}")
            
            # Show machine activity
            if st.session_state.transactions:
                machine_transactions = [t for t in st.session_state.transactions 
                                     if t['sender'] == machine or t['receiver'] == machine]
                if machine_transactions:
                    st.write('Recent Activity:')
                    st.dataframe(pd.DataFrame(machine_transactions).tail(5))

with tab3:
    st.header('Transaction Ledger')
    if st.session_state.transactions:
        st.dataframe(pd.DataFrame(st.session_state.transactions))
    else:
        st.info('No transactions recorded yet')

with tab4:
    st.header('Analytics')
    if st.session_state.transactions:
        df = pd.DataFrame(st.session_state.transactions)
        
        # Time series of transactions
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        daily_transactions = df.groupby(df['timestamp'].dt.date).size().reset_index()
        daily_transactions.columns = ['date', 'count']
        
        fig_timeline = px.line(daily_transactions, x='date', y='count',
                             title='Transaction Volume Over Time')
        st.plotly_chart(fig_timeline)
        
        # Risk score distribution
        fig_risk = px.histogram(df, x='ai_risk_score', nbins=20,
                              title='AI Risk Score Distribution')
        st.plotly_chart(fig_risk)
        
        # Machine interaction heatmap
        machine_interactions = pd.crosstab(df['sender'], df['receiver'])
        fig_heatmap = px.imshow(machine_interactions,
                               title='Machine Interaction Heatmap')
        st.plotly_chart(fig_heatmap)

# Footer
st.markdown('---')
st.markdown('M2M Transaction System - Powered by AI Agents and Blockchain')
