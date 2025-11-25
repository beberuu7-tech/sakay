from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Student
import re
from datetime import date

class DriverRegistrationForm(UserCreationForm):
    """Form for creating new driver accounts"""
    
    # User fields
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    
    # Driver fields
    driver_id = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., DRV-2024-001'}),
        help_text='Your unique driver ID'
    )
    
    license_number = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text='Valid driver\'s license number'
    )
    
    license_expiry = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        help_text='License expiration date'
    )
    
    phone_number = forms.CharField(
        max_length=17,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+639171234567'}),
        help_text='Format: +639XXXXXXXXX'
    )
    
    address = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )
    
    date_of_birth = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    
    emergency_contact_name = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    emergency_contact_number = forms.CharField(
        max_length=17,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+639171234567'})
    )
    
    profile_picture = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'})
    )
    
    # License documents
    license_photo = forms.ImageField(
        required=True,
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        help_text='Upload photo of your driver\'s license (Required for verification)'
    )
    
    accept_terms = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='I accept the terms and conditions'
    )
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
    
    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if not re.match(r'^\+639\d{9}$', phone):
            raise ValidationError('Phone number must be in format: +639XXXXXXXXX')
        return phone
    
    def clean_emergency_contact_number(self):
        phone = self.cleaned_data.get('emergency_contact_number')
        if not re.match(r'^\+639\d{9}$', phone):
            raise ValidationError('Phone number must be in format: +639XXXXXXXXX')
        return phone
    
    def clean_license_expiry(self):
        expiry = self.cleaned_data.get('license_expiry')
        if expiry and expiry < date.today():
            raise ValidationError('License has already expired.')
        return expiry
    
    def clean_date_of_birth(self):
        dob = self.cleaned_data.get('date_of_birth')
        if dob:
            today = date.today()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            if age < 21:
                raise ValidationError('Driver must be at least 21 years old.')
        return dob

class StudentRegistrationForm(UserCreationForm):
    """Form for creating new student accounts"""
    
    # User fields
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your first name'
        })
    )
    
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your last name'
        })
    )
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your.email@example.com'
        })
    )
    
    # Student profile fields
    student_id = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., STU-2024-001'
        }),
        help_text='Your unique student ID number'
    )
    
    phone_number = forms.CharField(
        max_length=17,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+639171234567'
        }),
        help_text='Format: +639XXXXXXXXX'
    )
    
    address = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Complete home address (Barangay, Municipality, Province)'
        })
    )
    
    date_of_birth = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        help_text='Your date of birth'
    )
    
    profile_picture = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*'
        }),
        help_text='Optional: Upload your photo (max 5MB)'
    )
    
    # Guardian information
    guardian_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Full name of parent/guardian'
        })
    )
    
    guardian_contact = forms.CharField(
        max_length=17,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+639171234567'
        }),
        help_text='Guardian phone number'
    )
    
    guardian_relationship = forms.ChoiceField(
        choices=[
            ('', 'Select relationship'),
            ('father', 'Father'),
            ('mother', 'Mother'),
            ('guardian', 'Legal Guardian'),
            ('sibling', 'Sibling'),
            ('other', 'Other')
        ],
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    # Emergency contact
    emergency_contact_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Emergency contact person'
        })
    )
    
    emergency_contact_number = forms.CharField(
        max_length=17,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+639171234567'
        }),
        help_text='Emergency contact phone number'
    )
    
    emergency_contact_relationship = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., Aunt, Uncle, Friend'
        })
    )
    
    # Terms and conditions
    accept_terms = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label='I accept the terms and conditions'
    )
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Choose a username'
            }),
            'password1': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Create a strong password'
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Confirm your password'
            }),
        }
    
    def clean_phone_number(self):
        """Validate phone number format"""
        phone = self.cleaned_data.get('phone_number')
        if not re.match(r'^\+639\d{9}$', phone):
            raise ValidationError('Phone number must be in format: +639XXXXXXXXX')
        return phone
    
    def clean_guardian_contact(self):
        """Validate guardian phone number"""
        phone = self.cleaned_data.get('guardian_contact')
        if not re.match(r'^\+639\d{9}$', phone):
            raise ValidationError('Phone number must be in format: +639XXXXXXXXX')
        return phone
    
    def clean_emergency_contact_number(self):
        """Validate emergency contact phone number"""
        phone = self.cleaned_data.get('emergency_contact_number')
        if not re.match(r'^\+639\d{9}$', phone):
            raise ValidationError('Phone number must be in format: +639XXXXXXXXX')
        return phone
    
    def clean_email(self):
        """Check if email is already registered"""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('This email is already registered.')
        return email
    
    def clean_student_id(self):
        """Check if student ID is unique"""
        student_id = self.cleaned_data.get('student_id')
        if Student.objects.filter(student_id=student_id).exists():
            raise ValidationError('This student ID is already registered.')
        return student_id
    
    def clean_date_of_birth(self):
        """Validate age (must be at least 5 years old)"""
        from datetime import date, timedelta
        dob = self.cleaned_data.get('date_of_birth')
        if dob:
            today = date.today()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            if age < 5:
                raise ValidationError('Student must be at least 5 years old.')
            if age > 100:
                raise ValidationError('Please enter a valid date of birth.')
        return dob
    
    def clean_profile_picture(self):
        """Validate image file size"""
        picture = self.cleaned_data.get('profile_picture')
        if picture:
            if picture.size > 5 * 1024 * 1024:  # 5MB
                raise ValidationError('Image file too large (max 5MB)')
        return picture


class StudentProfileUpdateForm(forms.ModelForm):
    """Form for updating student profile"""
    
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    
    guardian_relationship = forms.ChoiceField(
        choices=[
            ('father', 'Father'),
            ('mother', 'Mother'),
            ('guardian', 'Legal Guardian'),
            ('sibling', 'Sibling'),
            ('other', 'Other')
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    emergency_contact_relationship = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = Student
        fields = [
            'phone_number', 'address', 'date_of_birth', 'profile_picture',
            'guardian_name', 'guardian_contact',
            'emergency_contact_name', 'emergency_contact_number'
        ]
        widgets = {
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+639171234567'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'profile_picture': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'guardian_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'guardian_contact': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+639171234567'
            }),
            'emergency_contact_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'emergency_contact_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+639171234567'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
    
    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if not re.match(r'^\+639\d{9}$', phone):
            raise ValidationError('Phone number must be in format: +639XXXXXXXXX')
        return phone
    
    def clean_guardian_contact(self):
        phone = self.cleaned_data.get('guardian_contact')
        if not re.match(r'^\+639\d{9}$', phone):
            raise ValidationError('Phone number must be in format: +639XXXXXXXXX')
        return phone
    
    def clean_emergency_contact_number(self):
        phone = self.cleaned_data.get('emergency_contact_number')
        if not re.match(r'^\+639\d{9}$', phone):
            raise ValidationError('Phone number must be in format: +639XXXXXXXXX')
        return phone
    
    def save(self, commit=True):
        student = super().save(commit=False)
        
        # Update user fields
        if student.user:
            student.user.first_name = self.cleaned_data['first_name']
            student.user.last_name = self.cleaned_data['last_name']
            student.user.email = self.cleaned_data['email']
            if commit:
                student.user.save()
        
        if commit:
            student.save()
        
        return student


class StudentPasswordChangeForm(forms.Form):
    """Form for changing password"""
    
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter current password'
        }),
        label='Current Password'
    )
    
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter new password'
        }),
        label='New Password',
        help_text='Password must be at least 8 characters'
    )
    
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm new password'
        }),
        label='Confirm New Password'
    )
    
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
    
    def clean_old_password(self):
        """Validate current password"""
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password):
            raise ValidationError('Current password is incorrect.')
        return old_password
    
    def clean_new_password2(self):
        """Validate that passwords match"""
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        
        if password1 and password2:
            if password1 != password2:
                raise ValidationError('The two password fields must match.')
            if len(password1) < 8:
                raise ValidationError('Password must be at least 8 characters long.')
        
        return password2
    
    def save(self, commit=True):
        """Save the new password"""
        password = self.cleaned_data['new_password1']
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user