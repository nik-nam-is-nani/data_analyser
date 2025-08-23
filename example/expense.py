from flask import Blueprint, jsonify, request
from src.models.user import User, Expense, db
from datetime import datetime, timedelta
from sqlalchemy import func, and_
import calendar

expense_bp = Blueprint('expense', __name__)

@expense_bp.route('/add_expense', methods=['POST'])
def add_expense():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        username = data.get('username', '').strip()
        category = data.get('category', '').strip()
        amount = data.get('amount')
        week_date = data.get('week_date')
        
        # Validation
        if not username or not category or amount is None:
            return jsonify({'error': 'Username, category, and amount are required'}), 400
        
        try:
            amount = float(amount)
            if amount < 0:
                return jsonify({'error': 'Amount must be positive'}), 400
        except (ValueError, TypeError):
            return jsonify({'error': 'Amount must be a valid number'}), 400
        
        # Check if user exists
        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Parse week_date
        if week_date:
            try:
                week_date = datetime.strptime(week_date, '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
        else:
            # Default to current date
            week_date = datetime.now().date()
        
        # Create new expense
        new_expense = Expense(
            username=username,
            category=category,
            amount=amount,
            week_date=week_date
        )
        
        db.session.add(new_expense)
        db.session.commit()
        
        return jsonify({
            'message': 'Expense added successfully',
            'expense': new_expense.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@expense_bp.route('/get_expenses/<username>', methods=['GET'])
def get_expenses(username):
    try:
        # Check if user exists
        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Get all expenses for the user
        expenses = Expense.query.filter_by(username=username).order_by(Expense.week_date.desc()).all()
        
        return jsonify({
            'username': username,
            'expenses': [expense.to_dict() for expense in expenses],
            'total_expenses': len(expenses)
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@expense_bp.route('/weekly_summary/<username>', methods=['GET'])
def weekly_summary(username):
    try:
        # Check if user exists
        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Get the date range for the last week
        today = datetime.now().date()
        last_week_start = today - timedelta(days=7)
        
        # Query expenses from the last week
        expenses = Expense.query.filter(
            and_(
                Expense.username == username,
                Expense.week_date >= last_week_start,
                Expense.week_date <= today
            )
        ).all()
        
        # Group expenses by category and sum amounts
        category_totals = {}
        total_amount = 0
        
        for expense in expenses:
            category = expense.category
            amount = float(expense.amount)
            
            if category not in category_totals:
                category_totals[category] = 0
            
            category_totals[category] += amount
            total_amount += amount
        
        # Find the highest spending category
        highest_category = None
        highest_amount = 0
        if category_totals:
            highest_category = max(category_totals, key=category_totals.get)
            highest_amount = category_totals[highest_category]
        
        return jsonify({
            'username': username,
            'period': f'{last_week_start.isoformat()} to {today.isoformat()}',
            'category_summary': category_totals,
            'total_amount': round(total_amount, 2),
            'highest_category': {
                'category': highest_category,
                'amount': round(highest_amount, 2)
            } if highest_category else None,
            'expense_count': len(expenses)
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@expense_bp.route('/expenses/<int:expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    try:
        expense = Expense.query.get_or_404(expense_id)
        db.session.delete(expense)
        db.session.commit()
        
        return jsonify({'message': 'Expense deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@expense_bp.route('/expenses/<int:expense_id>', methods=['PUT'])
def update_expense(expense_id):
    try:
        expense = Expense.query.get_or_404(expense_id)
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Update fields if provided
        if 'category' in data:
            category = data['category'].strip()
            if category:
                expense.category = category
        
        if 'amount' in data:
            try:
                amount = float(data['amount'])
                if amount < 0:
                    return jsonify({'error': 'Amount must be positive'}), 400
                expense.amount = amount
            except (ValueError, TypeError):
                return jsonify({'error': 'Amount must be a valid number'}), 400
        
        if 'week_date' in data:
            try:
                week_date = datetime.strptime(data['week_date'], '%Y-%m-%d').date()
                expense.week_date = week_date
            except ValueError:
                return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
        
        db.session.commit()
        
        return jsonify({
            'message': 'Expense updated successfully',
            'expense': expense.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

