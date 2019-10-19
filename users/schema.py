from django.contrib.auth import get_user_model
from addiCore.models import Profile
import jwt
from django.core.mail import send_mail
from django.conf import settings
import graphene
from graphene_django import DjangoObjectType
from random import randint
from django.contrib.auth.hashers import check_password
from django.db.models import Q

def otpgenerate(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)


class ProfileType(DjangoObjectType):
    class Meta:
        model=Profile

class UserType(DjangoObjectType):
    class Meta:
        model=get_user_model()


class Query(graphene.ObjectType):
    user=graphene.Field(UserType, id=graphene.Int())
    me=graphene.Field(UserType)
    alluser = graphene.List(UserType)
    userprofile = graphene.Field(ProfileType, id=graphene.Int())
    searchuser=graphene.List(UserType, searchtext=graphene.String())
    randomuser = graphene.List(UserType)
    generateotp=graphene.String()

    def resolve_me(self,info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("notLoggedIn")    
        return user

    def resolve_user(self, info,id):
        return get_user_model().objects.get(id=id)

    def resolve_all_user(self, info):
        user = get_user_model()
        return user.objects.all()

    def resolve_userprofile(self, info, id):
        user = get_user_model().objects.get(id=id)
        print(user)
        try:
           return Profile.objects.get(user=user)
             
        except:
            raise Exception("Proflie DOes not exist")
    def resolve_searchuser(self, info, searchtext):
        criteria1 = ~Q(is_superuser = True)
        criteria2 = Q(username__icontains=searchtext)
        return get_user_model().objects.filter( criteria1 & criteria2 )


    def resolve_generateotp(self, info):
        user = info.context.user
        print(user)
        if user.is_anonymous:
            raise Exception("Log in to update profile")
        profile = Profile.objects.get(user=user)
        emailotp=otpgenerate(6)
        subject = 'Thank you for registering to our site, Your one time password is'
        message =  "Your otp is " + str(emailotp)
        recipient_list = [user.email]
        email_from = settings.EMAIL_HOST_USER
        mailsent=send_mail( subject, message, email_from, recipient_list )
        print(mailsent)
        if (mailsent):
            profile.emailotp=emailotp
            profile.save()
            return "Otp Sent"
        else:
            return "Mail not Sent"



class Updateprofile(graphene.Mutation):
    profile = graphene.Field(ProfileType)
    class Arguments:
        email=graphene.String()
        fullname=graphene.String()
        headerpic=graphene.String()
        profilepic=graphene.String()
        city=graphene.String()
        state=graphene.String()
        country=graphene.String()
        occupation=graphene.String()
        shortdescription=graphene.String()
        isPublic = graphene.Boolean()
        
    def mutate(self, info,email,fullname,city,state,country,occupation,shortdescription,headerpic,profilepic, isPublic):
        user = info.context.user
        print(user)
        if user.is_anonymous:
            raise Exception("Log in to update profile")
        profile = Profile.objects.get(user=user)
       
        
        profile.fullname=fullname
        profile.headerPic=headerpic
        profile.profilePic=profilepic
        profile.city=city
        profile.state=state
        profile.country=country
        profile.occupation=occupation
        profile.shortdescription=shortdescription
        profile.isPublic = isPublic
        profile.save()
        return Updateprofile(profile)


class CreateUser(graphene.Mutation):
    token = graphene.String()
    class Arguments:
        username=graphene.String()
        password = graphene.String()
        email=graphene.String()
        firstname=graphene.String()
        lastname=graphene.String()
    
    def mutate(self, info, username, password, email, firstname, lastname):
        try:
            user = get_user_model().objects.get(email=email)
            raise Exception("Email already registered")
        except:
            emailotp=otpgenerate(6)
            subject = 'Thank you for registering to our site, Your one time password is'
            message =  "Your otp is " + str(emailotp)
            recipient_list = [email]
            email_from = settings.EMAIL_HOST_USER
            mailsent=send_mail( subject, message, email_from, recipient_list )
            print(mailsent)
            if (mailsent):
                try:
                    user = get_user_model()(
                    username=username,
                    email=email
                    )
                    user.set_password(password)
                    user.save()
       
                    encoded_jwt = jwt.encode({'username': username}, 's)oavr10zqd&ws0vi4*k-s*du09o45#*7&#-b)bp-ldeh@@hx&', algorithm='HS256')
                    Profile.objects.create(user=user, emailotp=emailotp, fname=firstname, lname=lastname)
                    return CreateUser(encoded_jwt.decode('utf-8'))
                except:
                    raise Exception("Username is taken")
            else:
                raise Exception("Email not valid")


class VerifyEmail(graphene.Mutation):
    isVerified=graphene.Boolean()
    class Arguments:
        otp=graphene.String()

    def mutate(self, info, otp):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Log in to like")
        p=Profile.objects.get(user=user)
        if (p.emailotp==otp):
            print("Otp is correct")
            p.emailverified=True
            p.save()
            return VerifyEmail(isVerified=True)
        else:
            p.emailverified=False
            p.save()
            print ("Otp is incoreect")
            return VerifyEmail(isVerified=False)


class CustomLogin(graphene.Mutation):
    user=graphene.Field(UserType)
    token=graphene.String()
    class Arguments:
        username=graphene.String()
        password=graphene.String()

    def mutate(self, info, username, password):
        try:
            user=get_user_model().objects.get(username=username)
            
            pvalid = check_password(password, user.password)
            if pvalid:
                p=Profile.objects.get(user=user)
                if p.issuspended:
                    raise Exception("Your Account has been suspended")
                if p.is2fa:
                    emailotp=otpgenerate(6)
                    subject = 'Thank you for registering to our site, Your one time password is'
                    message =  "Your otp is " + str(emailotp)
                    recipient_list = [user.email]
                    email_from = settings.EMAIL_HOST_USER
                    mailsent=send_mail( subject, message, email_from, recipient_list )
                    print(mailsent)
                    p.emailotp = emailotp
                    p.save()
                    return CustomLogin(token="@FA is enabled", user=user)
                else:


                
                    encoded_jwt = jwt.encode({'username':user.username}, 's)oavr10zqd&ws0vi4*k-s*du09o45#*7&#-b)bp-ldeh@@hx&', algorithm='HS256')
                    return CustomLogin(token=encoded_jwt.decode('utf-8'), user=user)
            else:
                raise Exception("Invalid Password")
        except get_user_model().DoesNotExist:
            raise Exception("Invalid User")


class Verify2FA(graphene.Mutation):
    isVerified=graphene.Boolean()
    token=graphene.String()
    
    class Arguments:
        otp=graphene.String()
        username=graphene.String()
        
    def mutate(self, info, otp, username):
        try:
            user=get_user_model().objects.get(username=username)
            p=Profile.objects.get(user=user)
            if p.emailotp == otp:
                encoded_jwt = jwt.encode({'username':user.username}, 's)oavr10zqd&ws0vi4*k-s*du09o45#*7&#-b)bp-ldeh@@hx&', algorithm='HS256')
                return Verify2FA(token=encoded_jwt.decode('utf-8'), isVerified=True)
            else:
                raise Exception("Invalid OTP")
        except get_user_model().DoesNotExist:
            raise Exception("Invalid user")
        
        



class UpdatePassword(graphene.Mutation):
    status=graphene.Boolean()

    class Arguments:
        password=graphene.String()
        oldpassword=graphene.String()

    def mutate(self, info, password, oldpassword):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Unauthorized user")
            
            
        pvalid = check_password(oldpassword, user.password)
        if pvalid:
            user.set_password(password)
            user.save()
            return UpdatePassword(True)
        else:
            raise Exception("Invalid Password")


class ChangePassword(graphene.Mutation):
    status=graphene.Boolean()

    class Arguments:
        password=graphene.String()
       

    def mutate(self, info, password):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Unauthorized user")
            
            
       
        user.set_password(password)
        user.save()
        return UpdatePassword(True)
        

class UpdateTwoFa(graphene.Mutation):
    status=graphene.Boolean()

    class Arguments:
        value=graphene.Boolean()

    def mutate(self, info, value):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Unauthorized user")
        profile=Profile.objects.get(user=user)
        if value:
            profile.is2fa=True
            profile.save()
            return UpdateTwoFa(True)
        else:
            profile.is2fa=False
            profile.save()
            return UpdateTwoFa(True) 




class GenerateOtpForUser(graphene.Mutation):
    status=graphene.Boolean()

    class Arguments:
        username=graphene.String()

    def mutate(self, info, username):
        try:

            user=get_user_model().objects.get(username=username)
            emailotp=otpgenerate(6)
            subject = 'Thank you for registering to our site, Your one time password is'
            message =  "Your otp is " + str(emailotp)
            recipient_list = [user.email]
            email_from = settings.EMAIL_HOST_USER
            mailsent=send_mail( subject, message, email_from, recipient_list )
            print(mailsent)
            p=Profile.objects.get(user=user)
            p.emailotp=emailotp
            p.save()
            return GenerateOtpForUser(True)
        except:
            raise Exception("User not registered")


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_profile=Updateprofile.Field()
    verify_email=VerifyEmail.Field()
    custom_login = CustomLogin.Field()
    verify_2fa=Verify2FA.Field()
    update_password=UpdatePassword.Field()
    update_twofa=UpdateTwoFa.Field()
    generate_otp_for_user=GenerateOtpForUser.Field()
    change_password=ChangePassword.Field()
