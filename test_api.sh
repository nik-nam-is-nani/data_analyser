#!/bin/bash

echo "=== Expense Tracker API Testing ==="
echo "Testing all API endpoints..."
echo ""

BASE_URL="http://localhost:5003/api"
TEST_USER="testuser_$(date +%s)"
TEST_PASS="testpass123"

echo "Using test user: $TEST_USER"
echo ""

# Test 1: Signup
echo "1. Testing user signup..."
SIGNUP_RESPONSE=$(curl -s -X POST $BASE_URL/signup \
  -H "Content-Type: application/json" \
  -d "{\"username\": \"$TEST_USER\", \"password\": \"$TEST_PASS\"}")

echo "Response: $SIGNUP_RESPONSE"
echo ""

# Test 2: Login
echo "2. Testing user login..."
LOGIN_RESPONSE=$(curl -s -X POST $BASE_URL/login \
  -H "Content-Type: application/json" \
  -d "{\"username\": \"$TEST_USER\", \"password\": \"$TEST_PASS\"}")

echo "Response: $LOGIN_RESPONSE"
echo ""

# Test 3: Add Expense
echo "3. Testing add expense..."
ADD_EXPENSE_RESPONSE=$(curl -s -X POST $BASE_URL/add_expense \
  -H "Content-Type: application/json" \
  -d "{\"username\": \"$TEST_USER\", \"category\": \"Food\", \"amount\": 25.50, \"week_date\": \"$(date +%Y-%m-%d)\"}")

echo "Response: $ADD_EXPENSE_RESPONSE"
echo ""

# Test 4: Add another expense
echo "4. Testing add another expense..."
ADD_EXPENSE2_RESPONSE=$(curl -s -X POST $BASE_URL/add_expense \
  -H "Content-Type: application/json" \
  -d "{\"username\": \"$TEST_USER\", \"category\": \"Travel\", \"amount\": 45.00, \"week_date\": \"$(date +%Y-%m-%d)\"}")

echo "Response: $ADD_EXPENSE2_RESPONSE"
echo ""

# Test 5: Get all expenses
echo "5. Testing get all expenses..."
GET_EXPENSES_RESPONSE=$(curl -s -X GET $BASE_URL/get_expenses/$TEST_USER)

echo "Response: $GET_EXPENSES_RESPONSE"
echo ""

# Test 6: Weekly summary
echo "6. Testing weekly summary..."
WEEKLY_SUMMARY_RESPONSE=$(curl -s -X GET $BASE_URL/weekly_summary/$TEST_USER)

echo "Response: $WEEKLY_SUMMARY_RESPONSE"
echo ""

# Test 7: Get all users (admin endpoint)
echo "7. Testing get all users..."
GET_USERS_RESPONSE=$(curl -s -X GET $BASE_URL/users)

echo "Response: $GET_USERS_RESPONSE"
echo ""

echo "=== API Testing Complete ==="
echo ""
echo "If all tests show successful responses, your API is working correctly!"
echo "You can now integrate these endpoints with your frontend application."

