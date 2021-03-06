﻿// ***********************************************************************
// Copyright (c) 2008 Charlie Poole
//
// Permission is hereby granted, free of charge, to any person obtaining
// a copy of this software and associated documentation files (the
// "Software"), to deal in the Software without restriction, including
// without limitation the rights to use, copy, modify, merge, publish,
// distribute, sublicense, and/or sell copies of the Software, and to
// permit persons to whom the Software is furnished to do so, subject to
// the following conditions:
// 
// The above copyright notice and this permission notice shall be
// included in all copies or substantial portions of the Software.
// 
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
// EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
// MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
// NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
// LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
// OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
// WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
// ***********************************************************************

using NUnit.Framework.Interfaces;
using NUnit.Framework.Constraints;
using NUnit.Framework.Internal;
using NUnit.TestData;
using NUnit.TestUtilities;

#if NET_4_0 || NET_4_5
using System;
using System.Threading.Tasks;
#endif

#if NET_4_0
using Task = System.Threading.Tasks.TaskEx;
#endif

namespace NUnit.Framework.Assertions
{
    [TestFixture]
    public class AssertThatTests
    {
        [Test]
        public void AssertionPasses_Boolean()
        {
            Assert.That(2 + 2 == 4);
        }

        [Test]
        public void AssertionPasses_BooleanWithMessage()
        {
            Assert.That(2 + 2 == 4, "Not Equal");
        }

        [Test]
        public void AssertionPasses_BooleanWithMessageAndArgs()
        {
            Assert.That(2 + 2 == 4, "Not Equal to {0}", 4);
        }

        [Test]
        public void AssertionPasses_ActualAndConstraint()
        {
            Assert.That(2 + 2, Is.EqualTo(4));
        }

        [Test]
        public void AssertionPasses_ActualAndConstraintWithMessage()
        {
            Assert.That(2 + 2, Is.EqualTo(4), "Should be 4");
        }

        [Test]
        public void AssertionPasses_ActualAndConstraintWithMessageAndArgs()
        {
            Assert.That(2 + 2, Is.EqualTo(4), "Should be {0}", 4);
        }

        [Test]
        public void AssertionPasses_ReferenceAndConstraint()
        {
            bool value = true;
            Assert.That(ref value, Is.True);
        }

        [Test]
        public void AssertionPasses_ReferenceAndConstraintWithMessage()
        {
            bool value = true;
            Assert.That(ref value, Is.True, "Message");
        }

        [Test]
        public void AssertionPasses_ReferenceAndConstraintWithMessageAndArgs()
        {
            bool value = true;
            Assert.That(ref value, Is.True, "Message", 42);
        }

        [Test]
        public void AssertionPasses_DelegateAndConstraint()
        {
            Assert.That(new ActualValueDelegate<int>(ReturnsFour), Is.EqualTo(4));
        }

        [Test]
        public void AssertionPasses_DelegateAndConstraintWithMessage()
        {
            Assert.That(new ActualValueDelegate<int>(ReturnsFour), Is.EqualTo(4), "Message");
        }

        [Test]
        public void AssertionPasses_DelegateAndConstraintWithMessageAndArgs()
        {
            Assert.That(new ActualValueDelegate<int>(ReturnsFour), Is.EqualTo(4), "Should be {0}", 4);
        }

        private int ReturnsFour()
        {
            return 4;
        }

        [Test]
        public void FailureThrowsAssertionException_Boolean()
        {
            Assert.Throws<AssertionException>(() => Assert.That(2 + 2 == 5));
        }

        [Test]
        public void FailureThrowsAssertionException_BooleanWithMessage()
        {
            var ex = Assert.Throws<AssertionException>(() => Assert.That(2 + 2 == 5, "message"));
            Assert.That(ex.Message, Contains.Substring("message"));
        }

        [Test]
        public void FailureThrowsAssertionException_BooleanWithMessageAndArgs()
        {
            var ex = Assert.Throws<AssertionException>(() => Assert.That(2 + 2 == 5, "got {0}", 5));
            Assert.That(ex.Message, Contains.Substring("got 5"));
        }

        [Test]
        public void FailureThrowsAssertionException_ActualAndConstraint()
        {
            Assert.Throws<AssertionException>(() => Assert.That(2 + 2, Is.EqualTo(5)));
        }

        [Test]
        public void FailureThrowsAssertionException_ActualAndConstraintWithMessage()
        {
            var ex = Assert.Throws<AssertionException>(() => Assert.That(2 + 2, Is.EqualTo(5), "Error"));
            Assert.That(ex.Message, Contains.Substring("Error"));
        }

        [Test]
        public void FailureThrowsAssertionException_ActualAndConstraintWithMessageAndArgs()
        {
            var ex = Assert.Throws<AssertionException>(() => Assert.That(2 + 2, Is.EqualTo(5), "Should be {0}", 5));
            Assert.That(ex.Message, Contains.Substring("Should be 5"));
        }

        [Test]
        public void FailureThrowsAssertionException_ReferenceAndConstraint()
        {
            bool value = false;
            Assert.Throws<AssertionException>(() => Assert.That(ref value, Is.True));
        }

        [Test]
        public void FailureThrowsAssertionException_ReferenceAndConstraintWithMessage()
        {
            bool value = false;
            var ex = Assert.Throws<AssertionException>(() => Assert.That(ref value, Is.True, "message"));
            Assert.That(ex.Message, Contains.Substring("message"));
        }

        [Test]
        public void FailureThrowsAssertionException_ReferenceAndConstraintWithMessageAndArgs()
        {
            bool value = false;
            var ex = Assert.Throws<AssertionException>(() => Assert.That(ref value, Is.True, "message is {0}", 42));
            Assert.That(ex.Message, Contains.Substring("message is 42"));
        }

        [Test]
        public void FailureThrowsAssertionException_DelegateAndConstraint()
        {
            Assert.Throws<AssertionException>(() => Assert.That(new ActualValueDelegate<int>(ReturnsFive), Is.EqualTo(4)));
        }

        [Test]
        public void FailureThrowsAssertionException_DelegateAndConstraintWithMessage()
        {
            var ex = Assert.Throws<AssertionException>(() => Assert.That(new ActualValueDelegate<int>(ReturnsFive), Is.EqualTo(4), "Error"));
            Assert.That(ex.Message, Contains.Substring("Error"));
        }

        [Test]
        public void FailureThrowsAssertionException_DelegateAndConstraintWithMessageAndArgs()
        {
            var ex = Assert.Throws<AssertionException>(() => Assert.That(new ActualValueDelegate<int>(ReturnsFive), Is.EqualTo(4), "Should be {0}", 4));
            Assert.That(ex.Message, Contains.Substring("Should be 4"));
        }

        [Test]
        public void AssertionsAreCountedCorrectly()
        {
            ITestResult result = TestBuilder.RunTestFixture(typeof(AssertCountFixture));

            int totalCount = 0;
            foreach (TestResult childResult in result.Children)
            {
                int expectedCount = childResult.Name == "ThreeAsserts" ? 3 : 1;
                Assert.That(childResult.AssertCount, Is.EqualTo(expectedCount), "Bad count for {0}", childResult.Name);
                totalCount += expectedCount;
            }

            Assert.That(result.AssertCount, Is.EqualTo(totalCount), "Fixture count is not correct");
        }

        private int ReturnsFive()
        {
            return 5;
        }

#if NET_4_0 || NET_4_5
        [Test]
        public void AssertThatSuccess()
        {
            Assert.That(async () => await AsyncReturnOne(), Is.EqualTo(1));
        }

        [Test]
        public void AssertThatFailure()
        {
            Assert.Throws<AssertionException>(() =>
                Assert.That(async () => await AsyncReturnOne(), Is.EqualTo(2)));
        }

        [Test, Platform(Exclude="Linux", Reason="Intermittent failures on Linux")]
        public void AssertThatErrorTask()
        {
            var exception = Assert.Throws<InvalidOperationException>(() =>
                Assert.That(async () => await ThrowInvalidOperationExceptionTask(), Is.EqualTo(1)));

#if NET_4_5
            Assert.That(exception.StackTrace, Contains.Substring("ThrowInvalidOperationExceptionTask"));
#endif
        }

        [Test]
        public void AssertThatErrorGenericTask()
        {
            var exception = Assert.Throws<InvalidOperationException>(() =>
                Assert.That(async () => await ThrowInvalidOperationExceptionGenericTask(), Is.EqualTo(1)));

#if NET_4_5
        Assert.That(exception.StackTrace, Contains.Substring("ThrowInvalidOperationExceptionGenericTask"));
#endif
        }

        [Test]
        public void AssertThatErrorVoid()
        {
            var exception = Assert.Throws<InvalidOperationException>(() =>
                Assert.That(async () => { await ThrowInvalidOperationExceptionGenericTask(); }, Is.EqualTo(1)));

#if NET_4_5
        Assert.That(exception.StackTrace, Contains.Substring("ThrowInvalidOperationExceptionGenericTask"));
#endif
        }

        private static Task<int> AsyncReturnOne()
        {
            return Task.Run(() => 1);
        }

        private static async Task<int> ThrowInvalidOperationExceptionGenericTask()
        {
            await AsyncReturnOne();
            throw new InvalidOperationException();
        }

        private static async System.Threading.Tasks.Task ThrowInvalidOperationExceptionTask()
        {
            await AsyncReturnOne();
            throw new InvalidOperationException();
        }
#endif
    }
}
